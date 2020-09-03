from functools import total_ordering
from random import shuffle

BG = dict(
    b="#bbbbff",
    w="#bbbbbb",
    r="#ffbbbb",
    y="#ffffbb",
    g="#bbffbb",
)

@total_ordering
class Card:
    def __init__(self, value):
        self.value = value

    @property
    def bgcolor(self):
        return BG[self.value[0]]
    @property
    def val(self):
        return self.value[1:]

    def __lt__(self, other):
        return self.value < other.value
    def __eq__(self, other):
        return self.value == other.value

class Game:
    def __init__(self, p1, p2, b1, b2, discard, deck):
        self.p1 = [Card(x) for x in p1]  # p1 hand
        self.p2 = [Card(x) for x in p2]  # p2 hand
        self.b1 = [Card(x) for x in b1]  # p1 board
        self.b2 = [Card(x) for x in b2]  # p2 board
        self.discard = [Card(x) for x in discard]
        self.deck = [Card(x) for x in deck]


def new() -> Game:
    deck = []
    for color in 'gbryw':
        for card in ["*"]*3 + [str(x) for x in range(2,11)]:
            print(card)
            deck.append(color + card)
    shuffle(deck)
    print(deck)
    p1, p2 = [], []
    for x in range(8):
        p1.append(deck.pop())
        p2.append(deck.pop())
    print(p1)
    return Game(p1=p1, p2=p2, deck=deck, b1=[], b2=[], discard=[])
