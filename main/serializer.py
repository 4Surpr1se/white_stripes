from django.contrib.auth.models import User
from rest_framework import serializers


class CreateSuperUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_superuser(validated_data.get('username'),
                                             password=validated_data.get('password'))
        return user
