from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views

class RecipeViewsTest(TestCase):

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
        ...

    #category
    def test_view_category_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_status_code_404_ok(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertEquals(response.status_code, 404)

    # def test_recipe_category_view_loads_correct_template(self):
    #     response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))
    #     self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_recipe_category_template_show_no_recipes_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertIn(
            'Not Found',
            response.content.decode('utf-8')
        )

    #detail_recipe
    def test_view_recipe_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_view_return_status_code_404_ok(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1}))
        self.assertEquals(response.status_code, 404)

    # def test_recipe_view_loads_correct_template(self):
    #     response = self.client.get(reverse('recipes:category', kwargs={'id':1}))
    #     self.assertTemplateUsed(response, 'recipes/pages/recipe-view.html')

    def test_recipe__template_show_no_recipes_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1000}))
        self.assertIn(
            'Not Found',
            response.content.decode('utf-8')
        )