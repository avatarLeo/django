from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe
from recipes.models import Category, Recipe
from django.http.response import Http404
from django.http.response import HttpResponse

#{% url 'recipes:category' recipe.category.id %}

def category(request, category_id):
    
    # recipe = Recipe.objects.filter(category__id=category_id, is_published=True)

    # if not recipe:
    #     raise Http404('Essa categoria não existe')

    recipe = get_list_or_404(
        Recipe.objects.filter(category__id=category_id, is_published=True).order_by('id')
    )
    return render(request, 'recipes/pages/category.html', context={
            "recipe":recipe,
            "title": f'{recipe[0].category.name} - Category |'
        })
    # return render(request, 'recipes/pages/category.html', context={
    #     "recipe":recipe,
    #     "title": f'{recipe.first().category.name} - Category |'
    # })

def home(request):
    
    recipe = Recipe.objects.filter(is_published=True).order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        "recipe":recipe
    })


def recipe(request, id):

    recipe = get_object_or_404(
        Recipe.objects.filter(id=id, is_published=True)
    )
    return render(request, 'recipes/pages/recipe-view.html', context={
        "recipe":recipe,
        "is_detail_page": True,
    })
