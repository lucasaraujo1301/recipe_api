from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        """
        The setUp function is run before every test in the class.
        It creates a new client, and then uses that client to log in as an admin user.
        The admin user is created using the create_superuser method of Django's built-in User model.

        :param self: Access the class variables and methods
        :return: Nothing
        :doc-author: Trelent
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="testpass123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123", name="Test User"
        )

    def test_users_list(self):
        """
        The test_users_list function is a test case for the admin site.
        It checks that the user list view contains our created user's name and email address.

        :param self: Access the class attributes in the test_users_list function
        :return: The user's name and email
        :doc-author: Trelent
        """
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """
        The test_edit_user_page function tests that the edit user page works.
        It does this by:
        - Getting the URL for editing a user (note that we are using the helper function reverse to build the URL since
            it will contain the URL to edit a user)
        - Making a GET request to that URL
        - Asserting that response gives back an HTTP 200 status code and contains both email and name of our test user

        :param self: Represent the instance of the class
        :return: A status code of 200 and the user's email and name
        :doc-author: Trelent
        """
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)
