import pytest

from recipes_app.models import Recipe


@pytest.mark.django_db
def test_recipe_string_representation(user):
    recipe = Recipe.objects.create(
        title="Super Pancake",
        description="Delicious",
        author=user
    )

    assert str(recipe) == "Super Pancake"
