from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.http.response import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

from utils.pagination import make_pagination

import os

PER_PAGE = int(os.environ.get('PER_PAGE', 10))

def category(request, category_id):
    
    recipe = get_list_or_404(
        Recipe.objects.filter(category__id=category_id, is_published=True).order_by('id')
    )
    pagination_range, page_obj = make_pagination(
        request=request,
        recipe=recipe,
        number_of_pages=PER_PAGE
        )
    return render(request, 'recipes/pages/category.html', context={
            "recipes": page_obj,
            "pagination_range": pagination_range,
            "title": f'{recipe[0].category.name} - Category |'  
        })

def home(request):
    
    recipe = Recipe.objects.filter(is_published=True).order_by('-id')

    pagination_range, page_obj = make_pagination(
        request=request,
        recipe=recipe,
        number_of_pages=PER_PAGE
        )
    messages.success(request, 'Bem vindo')
    messages.info(request, 'Bem vindo')
    messages.error(request, 'Bem vindo')
    return render(request, 'recipes/pages/home.html', context={
        "recipes":page_obj,
        "pagination_range": pagination_range
    })


def recipe(request, id):

    recipe = get_object_or_404(
        Recipe.objects.filter(id=id, is_published=True)
    )
    return render(request, 'recipes/pages/recipe-view.html', context={
        "recipe":recipe,
        "is_detail_page": True,
    })

def search(request):    
    search_term = request.GET.get('search', '').strip()
    if not search_term:
        raise Http404('Receita não encontrada')

    recipe = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')
    
    pagination_range, page_obj = make_pagination(
        request=request,
        recipe=recipe,
        number_of_pages=PER_PAGE
        )
    return render(
        request,
        'recipes/pages/search.html',
        context={
            'page_title': f'Buscando por {search_term}',
            'search_term': search_term,
            'recipes':page_obj,
            'pagination_range': pagination_range,
            'additional_url_query': f'&search={search_term}',
            'teste': 'Contexto esta ok'
        }
    )
