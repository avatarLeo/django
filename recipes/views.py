from django.shortcuts import render
from utils.recipes.factory import make_recipe
from recipes.models import Category, Recipe

#{% url 'recipes:category' recipe.category.id %}

def category(request, category_id):
    
    recipe = Recipe.objects.filter(category__id=category_id, is_published=True)

    return render(request, 'recipes/pages/category.html', context={
        "recipe":recipe
    })

def home(request):
    
    recipe = Recipe.objects.filter(is_published=True).order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        "recipe":recipe
    })


def recipe(request, id):

    recipe = Recipe.objects.get(id=id)
    return render(request, 'recipes/pages/recipe-view.html', context={
        "recipe":recipe
    })
