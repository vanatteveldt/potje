from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'game/', views.GamesListView.as_view(), name='games_list'),
    path(r'game/new', views.GamesCreateView.as_view(), name='games_new'),
    path(r'game/<int:pk>/<int:player>/<code>', views.game, name='game'),
    path(r'game/<int:pk>', views.GameOverview.as_view(), name='game_overview'),
    path(r'game/<int:pk>/claim/<int:player>', views.GameClaim.as_view(), name='game_claim'),

]
