from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


USER_MODEL = get_user_model()


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = USER_MODEL.objects.create_superuser(
            email="admin_user@mail.com",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)

        self.user = USER_MODEL.objects.create_user(
            email="test_user@mail.com",
            password="testuser123",
            name="Test User Name"
        )

    def test_user_listed(self):
        """ test user in admin listing """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_change_user(self):
        """ Test that user edit page works """
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_add_user(self):
        """ Test that user add page works """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
