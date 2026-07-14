from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase

class RecipeDtailViewsTest(RecipeTestBase):

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