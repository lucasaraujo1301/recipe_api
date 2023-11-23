from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """
        The create function is used to create a new user.
        It takes the validated data and creates a new user object using the create_user function from Django's built-in
         User model.
        The **validated_data argument unpacks all the key/value pairs in validated_data into keyword arguments for
         create_user.

        :param self: Refer to the current instance of the class
        :param validated_data: Pass the data that has been validated by the serializer
        :return: A user object
        :doc-author: Trelent
        """
        return get_user_model().objects.create_user(**validated_data)
