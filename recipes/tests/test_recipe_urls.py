from django.urls import reverse
from django.test import TestCase

class RecipeURLsTest(TestCase):

    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEquals(url, '/')


    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', args=(1,))
        self.assertEquals(url, '/recipes/category/1/')

    def test_recipe_recipes_url_is_correct(self):
        url = reverse('recipes:recipe', args=(1,))
        self.assertEquals(url, '/recipes/1/')