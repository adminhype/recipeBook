from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from recipes_app.models import Recipe


class RecipeAPITestCase(APITestCase):

    def test_get_recipes_list(self):
        url = '/recipes-list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recipe(self):

        user = User.objects.create_user(
            username='testuser', password='password123')

        url = '/recipes-list/'

        data = {
            'title': 'pancakes',
            'description': 'milk, eggs, sugar, flour',
            'author': user.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
