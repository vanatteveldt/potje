from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'game/<name>/<player>', views.game, name='game')
]
