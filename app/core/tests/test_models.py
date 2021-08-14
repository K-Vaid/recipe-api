from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


USER_MODEL = get_user_model()


# Helper functions
def sample_user(email='test_usr@mail.com', password='testuser'):
    """ Create sample user """
    return USER_MODEL.objects.create_user(email, password)


class ModelTests(TestCase):
    def test_new_user_creating_with_email(self):
        """ Test creating a new user with email is successful """
        email = "Test_uzr@yopmail.com"
        password = "TestUsr123"
        user = USER_MODEL.objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Check if the email is normalized for new user """
        email = "new_us@GMAIL.COM"
        user = USER_MODEL.objects.create_user(
            email=email,
            password="Test1234"
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Check if blank email raises ValueError for new user """
        with self.assertRaises(ValueError):
            USER_MODEL.objects.create_user(None, 'hue2323c4')

    def test_create_new_superuser(self):
        """ Test creating a new Superuser """
        user = USER_MODEL.objects.create_superuser(
            'test@yopmial.com',
            'dhahdas3hh'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ Test the tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
