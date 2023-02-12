from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from . import models, forms

import re
import math

def index(request):

    if request.method == 'POST':
        form = forms.HistributionForm(request.POST)
        if form.is_valid():
            form.save()

    latestArticles = models.Article.objects.order_by('date')[:6]
    form = forms.HistributionForm()

    context = {
        'latestArticles' : latestArticles,
        'form': form
    }
    return render(request, 'index.html', context)


def detailArticle(request, articleId):
    article = models.Article.objects.get(id = articleId)
    footerImages = []

    if(article.isBigFormat):
        images = article.images.all()[3:]
    else:
        images = article.images.all()[2:]

    MIN_PARAGRAPHS_IN_LINE = 1

    paragraphs = article.text.strip("\n").split("\n")
    if(len(paragraphs) == 1):
        paragraphs = re.split("(?<=(?<=[^A-ZА-ЯЁ])\. )", article.text)
        MIN_PARAGRAPHS_IN_LINE:int = 2

    paragraphs = _reduceParagraphs(paragraphs, MIN_PARAGRAPHS_IN_LINE)            
 
    imagesLen = len(images)
    if(imagesLen != 0):
        # paragraphsLen = math.floor(len(paragraphs)/MIN_PARAGRAPHS_IN_LINE)
        paragraphsLen = len(paragraphs)
        print("parLen: ", paragraphsLen)
        print("imLen: ", imagesLen)
        ratio = (paragraphsLen-1)/imagesLen
        print(ratio)
        number = 0
        if(ratio < 1):
            while(ratio < 1):
                imagesLen -= 1
                number += 1
                ratio = paragraphsLen-1/imagesLen
            
            footerImages = images[number:]
            images = images[:number]
        else:
            lastItem = paragraphs[-1]
            paragraphs = _reduceParagraphs(paragraphs[:-1], math.ceil(ratio), False)
            paragraphs.append(lastItem)

    context = {
        'article': article,
        'paragraphs': paragraphs,
        'imagesInParagraphs': images,
        'footerImages': footerImages,
    }
    # print(images[0].image.url)
    # print(footerImages[0].image.url)

    print("len footer: ", len(footerImages))
    print("len paragraph: ", len(images))

    return render(request, 'detailArticle.html', context)


def mapPage(request):
    return render(request, 'map.html')


def qrPage(request):
    return render(request, 'qr.html')


def allPage(request):
    articles = models.Article.objects.all()
    context = {
        "articles": articles
    }
    return render(request, 'all.html', context)


class SearchResultsView(ListView):
    model = models.Article
    template_name = "searchResults.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = models.Article.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return object_list

def searchPage(request):
    results = []

    if request.method == "GET":
        query = request.GET.get('q')
        results = models.Article.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'searchResults.html', {'query': query, 'articles': results})


def _reduceParagraphs(paragraphs:list, min:int, redeceInEnd = True):
    if(min != 1):
        for i in range(math.floor(len(paragraphs)/min)):
            for j in range(min-1):
                paragraphs[i] = paragraphs[i] + (paragraphs[i+1])
                paragraphs.pop(i+1)

        if(len(paragraphs) != 1 and redeceInEnd):
            if(len(paragraphs[-1]) != len(paragraphs[-2])):
                paragraphs[-2] = paragraphs[-2] + paragraphs[-1]
                paragraphs.pop(-1)

    return paragraphs