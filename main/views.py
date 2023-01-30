from django.http import HttpResponse
from django.shortcuts import render
from . import models

def index(request):
    latestArticles = models.Article.objects.order_by('date')[:5]
    context = {
        'latestArticles' : latestArticles
    }
    return render(request, 'index.html', context)

def detailArticle(request, articleId):
    article = models.Article.objects.get(id = articleId)
    # photos = article.images.all[1:]
    # print(photos)
    context = {
        'article': article
    }
    return render(request, 'detailArticle.html', context)

def mapPage(request):
    return render(request, 'map.html')

def qrPage(request):
    return render(request, 'qr.html')