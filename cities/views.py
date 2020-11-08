from django.forms import Form, CharField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, RedirectView, DetailView, FormView

from cities.models import Game, new_game


def index(request):
    games = list(Game.objects.only('name'))
    return render(request, "index.html")


class GameOverview(DetailView):
    model = Game
    object: Game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = ("Waiting for players to join"
                             if None in [self.object.p1_name, self.object.p2_name]
                             else f"Player {self.object.active_player}'s turn")
        return context

def game(request, pk, player, code):
    g = Game.objects.get(pk=pk)
    correct_code = getattr(g, f"p{player}_code")
    opponent = 1 if player == 2 else 2
    if not code == correct_code:
        raise Exception("Invalid code")
    context = dict(
        name=getattr(g, f"p{player}_name"),
        player=player,
        hand=sorted(getattr(g, f"p{player}_hand")),
        ndeck=len(g.deck),
        board=sorted(getattr(g, f"p{player}_board")),
        opponent_board=sorted(getattr(g, f"p{opponent}_board")),
        discard=g.discard,
    )
    return render(request, "game.html", context)


class GameClaim(FormView):
    template_name = "cities/game_claim.html"
    class form_class(Form):
        player_name = CharField()
        password = CharField()

    def get_initial(self):
        initial = super().get_initial()
        object = Game.objects.get(pk=self.kwargs['pk'])
        player = self.kwargs['player']
        initial['player_name'] = getattr(object, f"p{player}_name")
        return initial

    def form_valid(self, form):
        object = Game.objects.get(pk=self.kwargs['pk'])
        player = self.kwargs['player']
        if getattr(object, f"p{player}_code") is None:
            setattr(object, f"p{player}_code", form.cleaned_data['password'])
            setattr(object, f"p{player}_name", form.cleaned_data['player_name'])
            object.save()
        url = reverse("game", kwargs=dict(pk=object.pk, player=player, code=form.cleaned_data['password']))
        return HttpResponseRedirect(url)

    def get_success_url(self):
        object = Game.objects.get(pk=self.kwargs['pk'])
        player = self.kwargs['player']
        return

class GamesListView(ListView):
    model = Game


class GamesCreateView(CreateView):
    model = Game
    fields = ['name']

    def form_valid(self, form):
        name = form.cleaned_data['name']
        print("!", name)
        self.object = new_game(name=name)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        print(reverse('game_overview', kwargs=dict(pk=self.object.pk)))
        return reverse('game_overview', kwargs=dict(pk=self.object.pk))
