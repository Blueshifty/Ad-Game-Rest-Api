from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'email', 'password', 'first_name', 'last_name', 'sex', 'phone_number', 'date_of_birth',
                  'profession')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    # token = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user_name = data.get("user_name", None)
        password = data.get("password", None)
        user = authenticate(user_name=user_name, password=password)
        if user is None:
            raise serializers.ValidationError(
                'Username or Password is Wrong.'
            )
        try:
            refresh = RefreshToken.for_user(user)
            # payload = api_settings.JWT_PAYLOAD_HANDLER(user)
            # jwt_token = api_settings.JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User not found. Password or Username Wrong'
            )
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_name': user.user_name,
        }
