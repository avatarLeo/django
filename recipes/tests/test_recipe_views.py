from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from recipes.models import Category, Recipe
from django.contrib.auth.models import User

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

    def test_view_home_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_return_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEquals(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_show_no_recipes_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No there recipes',
            response.content.decode('utf-8')
        )
    def test_recipe_home_templates_loads_recipes(self):
        self.make_recipe()        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('Recipe title', content)

    def test_recipe_home_templates_no_loads_not_published_recipes(self):
        title = 'Test no published'
        self.make_recipe(title=title, is_published=False)        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertNotIn(title, content)

    #category
    def test_view_category_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_status_code_404_ok(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertEquals(response.status_code, 404)

    def test_recipe_category_is_not_published_and_return_status_code_404(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': recipe.category.id})
        )
        self.assertEquals(response.status_code, 404)

    def test_recipe_category_view_loads_correct_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_recipe_category_templates_loads_recipe(self):
            needed_category_test = 'This is a test category'
            self.make_recipe(title=needed_category_test)
            response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))
            content = response.content.decode('utf-8')

            self.assertIn(needed_category_test, content)

    def test_recipe_category_template_show_no_recipes_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertIn(
            'Not Found',
            response.content.decode('utf-8')
        )

    #detail_recipe
    def test_view_recipe_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_view_return_status_code_404_ok(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1000}))
        self.assertEquals(response.status_code, 404)

    def test_detail_recipe_is_not_published_return_404(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe__template_show_no_recipes_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1000}))
        self.assertIn(
            'Not Found',
            response.content.decode('utf-8')
        )

    def test_recipe_detail_templates_loads_correct_recipe(self):
        needed_category_test = 'This is a detail page'
        self.make_recipe(title=needed_category_test)
        response = self.client.get(
                reverse('recipes:recipe', kwargs={'id':1})
            )
        content = response.content.decode('utf-8')

        self.assertIn(needed_category_test, content)
    