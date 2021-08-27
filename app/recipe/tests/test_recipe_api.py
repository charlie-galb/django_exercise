from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Some dish',
        'description': 'A relevant description'
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)


def detail_url(recipe_id):
    """Return recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


class RecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe()
        sample_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(
            res.data[0].get('name'), serializer.data[0].get('name')
            )

    def test_retrieve_single_recipe(self):
        """Test retrieving a single recipe"""
        recipe = sample_recipe()
        url = detail_url(recipe.id)

        res = self.client.get(url)
        serializer = RecipeSerializer(recipe, many=False)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Thai green curry',
            'description': 'Cook peppers and tofu in coconut milk and serve.'
        }
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(recipe.name, payload.get('name'))
