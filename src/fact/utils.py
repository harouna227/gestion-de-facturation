from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

from fact.models import Facture


def pagination(request, factures):
    default_page = 1
    page = request.GET.get('page', default_page)
    item_per_page = 3
    paginator = Paginator(factures, item_per_page) 
    try:
        items_page =  paginator.page(page)
    except PageNotAnInteger:
        items_page =  paginator.page(default_page)
    except EmptyPage:
        items_page =  paginator.page(paginator.num_page)
    
    return items_page


def get_facture(pk):
    obj = Facture.objects.get(pk=pk)
    articles = obj.article_set.all()   
    context = {
        'obj': obj,
        'articles': articles
    }
    return context