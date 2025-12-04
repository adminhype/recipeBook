import pytest

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.urls import reverse
from django.contrib.auth.models import User

from recipes_app.models import Recipe


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='chef', password='password123')


@pytest.fixture
def auth_client(api_client, user):
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client


@pytest.mark.django_db
def test_create_recipe_without_auth(api_client, user):
    url = reverse('recipe-list')
    recipe_data = {
        'title': 'forbidden pancake',
        'description': 'This recipe should not be created',
        'author': user.id
    }
    response = api_client.post(url, recipe_data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_recipe_detail_without_auth(api_client, user):
    recipe = Recipe.objects.create(
        title='unauthorized soup',
        description='not for public',
        author=user
    )
    url = reverse('recipe-detail-detail', kwargs={'pk': recipe.id})
    response = api_client.get(url, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_recipes_list(auth_client):
    url = reverse('recipe-list')
    response = auth_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_recipe_with_auth(auth_client, user):
    url = reverse('recipe-list')
    recipe_data = {
        'title': 'steak',
        'description': 'only for meat lovers',
        'author': user.id
    }
    response = auth_client.post(url, recipe_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Recipe.objects.count() == 1
    assert Recipe.objects.get().author == user


@pytest.mark.django_db
def test_get_recipe_detail(auth_client, user):
    recipe = Recipe.objects.create(
        title='veggie salad',
        description='healthy and fresh',
        author=user
    )
    url = reverse('recipe-detail-detail', kwargs={'pk': recipe.id})
    response = auth_client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'veggie salad'
    assert response.data['description'] == 'healthy and fresh'
    assert response.data['author'] == user.id
