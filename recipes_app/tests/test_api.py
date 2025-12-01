from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User
from recipes_app.models import Recipe


class RecipeAPITestCaseUnhappy(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='pass', password='password123')
        self.url = '/recipes-list/'

        self.recipe_data = {
            'title': 'forbidden pancake',
            'description': 'This recipe should not be created',
            'author': self.user.id
        }

    def test_create_recipe_without_auth(self):
        response = self.client.post(self.url, self.recipe_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RecipeAPITestCaseHappy(APITestCase):

    def setUp(self):
        self.url = '/recipes-list/'

    def test_get_recipes_list(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
