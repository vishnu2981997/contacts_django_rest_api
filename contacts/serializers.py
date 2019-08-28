from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *


class UserSerializer(serializers.ModelSerializer):
    # contacts = serializers.PrimaryKeyRelatedField(many=True, queryset=Contact.objects.all())
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        # user.is_active = False
        # user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class ContactSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    name = serializers.CharField(
        required=True,
        allow_null=False
    )
    email = serializers.EmailField(
        required=True,
        allow_null=False
    )
    number = serializers.CharField(
        min_length=10,
        max_length=10,
        required=True,
        allow_null=False
    )

    # For displaying error messages

    def __init__(self, *args, **kwargs):
        super(ContactSerializer, self).__init__(*args, **kwargs)

    def validate_name(self, name: str) -> str:
        if len(name) > 32:
            raise serializers.ValidationError('Kindly enter a valid name (max 32 characters)')
        if len(Contact.objects.filter(owner=self.context['request'].user, name=name)) > 0:
            raise serializers.ValidationError('Contact with this name already exists.')
        return name

    def validate_email(self, email: str) -> str:
        if len(Contact.objects.filter(owner=self.context['request'].user, email=email)) > 0:
            raise serializers.ValidationError('Contact with this number already exists.')
        return email

    def validate_number(self, number: str) -> str:
        if not number.isdigit():
            raise serializers.ValidationError('Kindly enter a valid mobile number.')
        if len(number) < 10:
            raise serializers.ValidationError('Kindly enter a 10 digit valid mobile number.')
        if len(Contact.objects.filter(owner=self.context['request'].user, number=number)) > 0:
            raise serializers.ValidationError('Contact with this number already exists.')
        return number

    class Meta:
        model = Contact
        fields = ["owner", "id", "name", "email", "number", "image", "created"]
