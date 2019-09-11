from rest_framework import serializers

from .models import *


class ContactNumberSerializer(serializers.ModelSerializer):
    number = serializers.CharField(
        min_length=10,
        max_length=10,
        required=True,
        allow_null=False
    )

    # For displaying error messages

    def __init__(self, *args, **kwargs):
        super(ContactNumberSerializer, self).__init__(*args, **kwargs)

    def validate_number(self, number: str) -> str:
        if not number.isdigit():
            raise serializers.ValidationError('Kindly enter a valid mobile number.')
        if len(number) < 10:
            raise serializers.ValidationError('Kindly enter a 10 digit valid mobile number.')
        if len(ContactNumber.objects.filter(contact__owner=self.context['request'].user, number=number)) > 0:
            raise serializers.ValidationError('ContactDetail with this number already exists.')
        return number

    class Meta:
        model = ContactDetail
        fields = ["number"]
        read_only = ["contact"]


class ContactDetailSerializer(serializers.ModelSerializer):
    contact_numbers = ContactNumberSerializer(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    name = serializers.CharField(
        required=True,
        allow_null=False
    )
    email = serializers.EmailField(
        required=True,
        allow_null=False
    )

    # For displaying error messages

    def __init__(self, *args, **kwargs):
        super(ContactDetailSerializer, self).__init__(*args, **kwargs)

    def validate_name(self, name: str) -> str:
        if len(name) > 32:
            raise serializers.ValidationError('Kindly enter a valid name (max 32 characters)')
        if len(ContactDetail.objects.filter(owner=self.context['request'].user, name=name)) > 0:
            raise serializers.ValidationError('ContactDetail with this name already exists.')
        return name

    def validate_email(self, email: str) -> str:
        if len(ContactDetail.objects.filter(owner=self.context['request'].user, email=email)) > 0:
            raise serializers.ValidationError('ContactDetail with this number already exists.')
        return email

    def create(self, validated_data):
        numbers_data = validated_data.pop('contact_numbers')
        contact = ContactDetail.objects.create(**validated_data)
        for number in numbers_data:
            ContactNumber.objects.create(contact=contact, **number)
        return contact

    class Meta:
        model = ContactDetail
        fields = ["owner", "id", "name", "email", "contact_numbers", "image", "created"]
