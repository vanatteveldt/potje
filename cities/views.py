from django.shortcuts import render

from cities.game import Game, new
from cities.models import GameState


def index(request):
    games = list(GameState.objects.only('name'))
    return render(request, "index.html")

def game(request, name, player):
    try:
        gs = GameState.objects.get(name=name)
        g = Game(**gs.state)
    except GameState.DoesNotExist:
        g = new()
    context = dict(
        player = player,
        hand = sorted(g.p1 if player == 1 else g.p2),
        ndeck = len(g.deck),
        b1 = g.b1,
        b2 = g.b2,
        discard = g.discard,
    )
    return render(request, "game.html", context)

