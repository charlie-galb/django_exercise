from django.test import TestCase

from core import models


def sample_recipe():
    return models.Recipe.objects.create(
        name='Pizza',
        description='Put it in the oven',
        )


class ModelTests(TestCase):

    def test_recipe_str(self):
        """Test recipe string representation"""
        recipe = sample_recipe()
        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        """Test ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            name='Dough',
            recipe=sample_recipe()
        )
        self.assertEqual(str(ingredient), ingredient.name)
