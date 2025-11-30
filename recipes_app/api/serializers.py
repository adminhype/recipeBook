from rest_framework import serializers

from recipes_app.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'created_at', 'author']
