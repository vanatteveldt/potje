import random
from random import shuffle

from django.db import models
from django.db.models import Model, TextField, JSONField, IntegerField, CharField
from django.db.models.signals import post_init
from django.dispatch import receiver

from cities.card import Card


class Game(Model):
    name = CharField(max_length=255)
    state = JSONField()
    last_card = CharField(max_length=2, null=True)
    active_player = IntegerField()
    p1_code = CharField(max_length=255, null=True)
    p2_code = CharField(max_length=255, null=True)
    p1_name = CharField(max_length=255, null=True)
    p2_name = CharField(max_length=255, null=True)


@receiver(post_init, sender=Game)
def post_init(sender, instance, **kwargs):
    state = instance.state
    instance.p1_hand = [Card(x) for x in state['p1_hand']]
    instance.p2_hand = [Card(x) for x in state['p2_hand']]
    instance.p1_board = [Card(x) for x in state['p1_board']]
    instance.p2_board = [Card(x) for x in state['p2_board']]
    instance.discard = [Card(x) for x in state['discard']]
    instance.deck = [Card(x) for x in state['deck']]


def new_game(name: str, active_player: int = None) -> Game:
    deck = []
    for color in 'gbryw':
        for card in ["*"] * 3 + [str(x) for x in range(2, 11)]:
            deck.append(color + card)
    random.shuffle(deck)
    p1, p2 = [], []
    for x in range(8):
        p1.append(deck.pop())
        p2.append(deck.pop())
    state = dict(
        p1_hand=p1,
        p2_hand=p2,
        deck=deck,
        p1_board=[],
        p2_board=[],
        discard=[]
    )
    if active_player is None:
        active_player = random.choice([1, 2])
    return Game.objects.create(name=name, state=state, active_player=active_player)
