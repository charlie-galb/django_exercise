from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Some dish',
        'description': 'A relevant description',
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
        recipe1 = sample_recipe(name='Hot dog')
        recipe2 = sample_recipe(name='Burger')

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0].get('name'), recipe1.name)
        self.assertEqual(res.data[1].get('name'), recipe2.name)

    def test_retrieve_single_recipe(self):
        """Test retrieving a single recipe"""
        recipe = sample_recipe()
        url = detail_url(recipe.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.name, res.data.get('name'))

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Thai green curry',
            'description': 'Cook peppers and tofu in coconut milk and serve.',
            'ingredients': [
                {'name': 'Peppers'},
                {'name': 'Coconut milk'}
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(recipe.name, payload.get('name'))
        ingredients = Ingredient.objects.filter(recipe=res.data['id'])
        self.assertEqual(
            ingredients[0].name, payload.get('ingredients')[1].get('name')
            )
        self.assertEqual(
            ingredients[1].name, payload.get('ingredients')[0].get('name')
            )

    def test_delete_recipe(self):
        """Test deleting a recipe"""
        recipe = sample_recipe(
            name='Cheese sandwich',
            description='Place cheese between two slices of bread.'
            )
        url = detail_url(recipe.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(pk=recipe.id).exists())

    def test_update_recipe_name(self):
        """test updating a recipe's name"""
        recipe = sample_recipe()
        url = detail_url(recipe.id)
        payload = {'name': 'Updated sample recipe'}

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.data['name'], payload.get('name'))

    def test_update_recipe_ingredients(self):
        """test updating a recipe's ingredients"""
        recipe = sample_recipe()
        url = detail_url(recipe.id)
        Ingredient.objects.create(
            name='Ingredient1', recipe=recipe
            )
        new_ingredient1 = {'name': 'First updated ingredient'}
        new_ingredient2 = {'name': 'Second updated ingredient'}
        payload = {
            'ingredients': [
                new_ingredient1,
                new_ingredient2,
            ]
        }

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(len(res.data.get('ingredients')), 2)
        self.assertEqual(res.data['name'], recipe.name)
        self.assertIn(
            new_ingredient1['name'],
            res.data['ingredients'][1].get('name')
            )
        self.assertIn(
            new_ingredient2['name'],
            res.data['ingredients'][0].get('name')
            )
