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
        The function also sets the is_staff attribute to False, which means that this user will not be able to log in to
        Django’s admin site.

        :param self: Refer to the class itself
        :param email: Create a user with an email
        :param password: Set the password of the user
        :param **extra_fields: Pass in any additional fields that you want to add to the user model
        :return: A user object
        :doc-author: Trelent
        """
        user = self.model(email=email, **extra_fields)
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
