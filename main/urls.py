from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('article/<int:articleId>', views.detailArticle, name="detailArticle"),
    path('map', views.mapPage, name="map"),
    path('qr', views.qrPage, name="qr"),
    path('all', views.allPage, name="all"),
    path('search', views.searchPage, name="searchResults")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)