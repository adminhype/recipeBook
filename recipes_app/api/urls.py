from rest_framework.routers import DefaultRouter

from django.urls import path, include
from .views import RecipeViewSet

router = DefaultRouter()
router.register(r'recipes-list', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
]
