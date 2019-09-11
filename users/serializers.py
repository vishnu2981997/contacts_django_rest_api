from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    # contacts = serializers.PrimaryKeyRelatedField(many=True, queryset=ContactDetail.objects.all())
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True
    )

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        # user.is_active = False
        # user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
