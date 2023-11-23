from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    """
    The create_user function creates a user with the given username, email and password.


    :param **params: Pass in a dictionary of parameters to the create_user function
    :return: A user object
    :doc-author: Trelent
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """
        The test_create_user_success function tests that the create user API endpoint works as expected.
        It does this by making a POST request to the CREATE_USER_URL, passing in a payload containing valid data.
        The test then asserts that we get back a 201 response (indicating success), and that the user was created
         correctly.

        :param self: Refer to the class instance
        :return: A 201 status code,
        :doc-author: Trelent
        """
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload["email"])
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """
        The test_user_with_email_exists_error function tests that the create user API endpoint
        returns a 400 bad request status code if the email already exists in the database.
        It also checks that an error message is returned and that it contains &quot;Email already exist.

        :param self: Access the instance of the class
        :return: The status code of 400,
        :doc-author: Trelent
        """
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", res.data)
        self.assertIn("user with this email already exists.", res.data["email"])

    def test_password_too_short_error(self):
        """
        The test_password_too_short_error function tests that the user creation endpoint returns a 400 bad request error
         if the password is too short.
        It also asserts that an error message is returned and that no user was created.

        :param self: Access the instance of the class
        :return: A 400 status code and a message that the password is too short
        :doc-author: Trelent
        """
        payload = {"email": "test@example.com", "password": "pw", "name": "Test Name"}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", res.data)
        self.assertIn(
            "Ensure this field has at least 5 characters.", res.data["password"]
        )

        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)