from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from products.models import Product, ProductCategory, Basket

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store'
        return context

# def index(request):
#     contex = {'title': 'Store'}
#     return render(request, 'products/index.html', contex)

class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store-каталог'
        context['categories'] = ProductCategory.objects.all()
        return context


# def products(request, category_id = None, page_number = 1):
    
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    
#     per_page = 3
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)

#     context = {
#         'title': 'Store - каталог', 
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#         }

#     return render(request, 'products/products.html', context)

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])  
    
    # META['HTTP_REFERER'] - перенаправление на эту же страницу

@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

