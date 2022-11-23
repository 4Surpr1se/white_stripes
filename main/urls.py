from django.urls import path

from main.views import BuyAPIRetrieve, RetrieveItem, SuccessView, CancelView, SuperUserCreator

urlpatterns = [
    path("buy/<pk>", BuyAPIRetrieve.as_view()),
    path("item/<pk>", RetrieveItem.as_view()),
    path("success/", SuccessView.as_view()),
    path("cancel/", CancelView.as_view()),
    path("superusercreate/", SuperUserCreator.as_view())
]
