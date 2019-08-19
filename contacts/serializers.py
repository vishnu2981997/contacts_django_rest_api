from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    number = serializers.IntegerField(
        min_value=1000000000,
        max_value=9999999999,
        required=True,
        allow_null=False
    )

    # For displaying error messages

    def __init__(self, *args, **kwargs):
        super(ContactSerializer, self).__init__(*args, **kwargs)

    def validate_number(self, number: int) -> int:
        if len(str(number)) < 10:
            raise serializers.ValidationError('Kindly enter a 10 digit valid mobile number.')
        if Contact.objects.filter(owner=self.context['request'].user, number=number):
            raise serializers.ValidationError('Contact with this number already exists.')
        return number

    class Meta:
        model = Contact
        fields = ["owner", "id", "name", "email", "number", "file", "created"]


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
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
