from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


USER_MODEL = get_user_model()
INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):
    """ Test the publicially available ingredients API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required for retrieving Ingredients """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """ Test the authorized user ingredients api """

    def setUp(self):
        self.user = USER_MODEL.objects.create_user(
            email='te_usr@mail.com',
            password='testuser'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredient_list(self):
        """ Test retrieve Ingredient list """
        Ingredient.objects.create(user=self.user, name='Potato')
        Ingredient.objects.create(user=self.user, name='Pepper')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test that ingredients returned are limited to authenticated users"""
        user_2 = USER_MODEL.objects.create_user(
            email='new_tst@mail.com',
            password='newuser'
        )
        Ingredient.objects.create(user=user_2, name='Tomato')
        ingredient = Ingredient.objects.create(user=self.user, name='Clove')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
