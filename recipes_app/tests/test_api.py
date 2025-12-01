from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

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
        self.user = User.objects.create_user(
            username='chef', password='password123')
        self.token = Token.objects.create(user=self.user)

        self.recipe_data = {
            'title': 'steak',
            'description': 'only for meat lovers',
            'author': self.user.id
        }

    def test_get_recipes_list(self):
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recipe_with_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.url, self.recipe_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(Recipe.objects.get().author, self.user)
