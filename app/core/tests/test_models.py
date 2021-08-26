from django.test import TestCase

from core import models


class ModelTests(TestCase):

    def test_recipe_str(self):
        """Test recipe string representation"""
        recipe = models.Recipe.objects.create(
            name='Pizza',
            description='Put it in the oven',
        )
        self.assertEqual(str(recipe), recipe.name)
