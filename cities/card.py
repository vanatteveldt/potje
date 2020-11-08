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
