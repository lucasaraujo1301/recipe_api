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
