import requests
import stripe
from django.http import JsonResponse, Http404

from django.views.generic import TemplateView
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from main.models import Item
from main.serializer import CreateSuperUser

stripe.api_key = 'rk_test_51M5sn0IqhDMrOiRA8lEXgceSpXrNbGvLdMR0CRMAyfI9C4BdsvfMNjPm56WoLy3or95KxLah0rmYEgaYDiU4z25100J05QqVNX'


class BuyAPIRetrieve(RetrieveAPIView):
    """Создаем сессию и отдаем sessionId,
     цена умножается на сто, потому что поле страйпа unit_amount_decimal не учитывает значения после запятой,
     все ошибки drf хэндлерит сам"""
    queryset = Item.objects.all()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()

        session = stripe.checkout.Session.create(
            success_url="http://localhost:8000/success/",
            cancel_url="http://localhost:8000/cancel/",
            line_items=[{
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': obj.name,
                        'description': obj.description
                    },
                    'unit_amount_decimal': obj.price * 100,
                },
                'quantity': 1,
            }],
            mode="payment",
        )

        return JsonResponse({'sessionId': session['id']})


class RetrieveItem(TemplateView):
    """Здесь достаем sessionId через апи вьюшку и отдаем в шаблон,
     если айтема с таким id не существует, бросает ошибку"""
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buy_request = requests.get(f'http://127.0.0.1:8000/buy/{kwargs["pk"]}').json()

        if buy_request.get('detail') is not None:
            raise Http404("Item with this id doesn't exist")

        sessionid = buy_request['sessionId']
        context['session'] = stripe.checkout.Session.retrieve(sessionid).url

        return context


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class SuperUserCreator(CreateAPIView):
    serializer_class = CreateSuperUser
