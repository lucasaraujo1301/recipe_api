from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        The create_user function creates a new user with the given email and password.
        The function normalizes the email address by lowercase, then hashes the password using Django’s built-in
        set_password() method.
        Finally, we save() our newly created user to our database.

        :param self: Refer to the class itself
        :param email: Create a new user with the email address provided
        :param password: Set the password for the user
        :param **extra_fields: Pass in any additional fields that may be required by the user model
        :return: A user object
        :doc-author: Trelent
        """
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
