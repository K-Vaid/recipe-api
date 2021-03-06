from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


USER_MODEL = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for user objects """

    class Meta:
        model = USER_MODEL
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """
        return USER_MODEL.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Update the user, setting the password correctly and return it """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user authentication objects """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ Validate and authenticate user """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code="authentication")

        attrs['user'] = user
        return attrs
