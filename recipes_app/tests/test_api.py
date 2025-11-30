from rest_framework.test import APITestCase
from rest_framework import status


class RecipeAPITestCase(APITestCase):

    def test_get_recipes_list(self):
        url = '/recipes-list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
