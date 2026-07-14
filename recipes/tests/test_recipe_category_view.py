from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewsTest(RecipeTestBase):

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


    