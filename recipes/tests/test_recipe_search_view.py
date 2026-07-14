from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewsTest(RecipeTestBase):  
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_load_correct_template(self):
        url = reverse('recipes:search') + '?search=test'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_page_title_and_scape(self):
        url = reverse('recipes:search') + '?search="test"'
        response = self.client.get(url)
        self.assertIn(
            "Buscando por &quot;test&quot",
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe_one = self.make_recipe(
            title=title1,
            slug='one',
            author_data={'username': 'one'}
        )

        recipe_two = self.make_recipe(
            title=title2,
            slug='two',
            author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response_one = self.client.get(f'{search_url}?search={title1}')
        response_two = self.client.get(f'{search_url}?search={title2}')
        response_both = self.client.get(f'{search_url}?search=This')

        self.assertIn(recipe_one, response_one.context['recipes'])
        self.assertNotIn(recipe_two, response_one.context['recipes'])

        self.assertIn(recipe_two, response_two.context['recipes'])
        self.assertNotIn(recipe_one, response_two.context['recipes'])

        self.assertIn(recipe_one, response_both.context['recipes'])
        self.assertIn(recipe_two, response_both.context['recipes'])
        
       