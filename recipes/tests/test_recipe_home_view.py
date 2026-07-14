from django.urls import resolve, reverse
from recipes import views
from unittest.mock import patch

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewsTest(RecipeTestBase):

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


    @patch('recipes.views.PER_PAGE', new=5)
    def test_recipe_home_is_there_pagination_in_templates(self):
        for i in range(10):
            kwargs = {'slug': f's{i}', 'author_data': {'username':f'u{i}'}}
            self.make_recipe(**kwargs)        
        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 5)
        self.assertEqual(len(paginator.get_page(2)), 5)