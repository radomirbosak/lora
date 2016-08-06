#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, IntEnum, unique
from random import shuffle

class PlayerError(Exception):
    def __init__(self, message):
        super().__init__(message)

@unique
class Color(Enum):
    cerven   = 1
    zelen    = 2
    gula     = 3
    zalud    = 4

@unique
class Value(IntEnum):
    sedmicka = 7
    osmicka  = 8
    devina   = 9
    desina   = 10
    dolnik   = 11
    hornik   = 12
    kral     = 13
    eso      = 14

    def shift_value(self, shift):
        minimum = min(Value)
        maximum = max(Value)
        new_value = ((self.value - minimum + shift) % (maximum - minimum + 1)) + minimum
        for value in Value:
            if value.value == new_value:
                return value

    def previous_value(self):
        return self.shift_value(-1)

    def next_value(self):
        return self.shift_value(1)


class LoraGame(Enum):
    stychy          = 1
    cervene         = 2
    horniky         = 3
    cerveny_kral    = 4
    prvy_a_posledny = 5
    mala_lora       = 6
    zaludny_dolnik  = 7
    velka_lora      = 8

class Card():

    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return "{0.name} {1.name}".format(self.color, self.value)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value

    def previous_card(self):
        return Card(self.color, self.value.previous_value())

    def next_card(self):
        return Card(self.color, self.value.next_value())

class OwnedCard(Card):
    def __init__(self, color, value, owner=None):
        super().__init__(color, value)
        self.owner = owner


class Player():
    def __init__(self, hand):
        self.hand = hand
        self.pile = []


def deal(deck, players):
    shuffle(deck)
    try:
        while deck:
            for player in players:
                player.hand.append(deck.pop())
    except IndexError:
        raise RuntimeError("Uneven number of cards in deck")

def full_deck():
    return [Card(color, value) for color in Color for value in Value]

def double_deck():
    return full_deck() + full_deck()

def move_card(card, deck_src, deck_dest):
    deck_src.remove(card)
    deck_dest.append(card)

def player_put_card(card, player, deck_dest):
    player.hand.remove(card)
    deck_dest.append(OwnedCard(card.color, card.value, player))

class Game():

    def __init__(self):
        deck = full_deck()

        self.players = [Player() for _ in range(4)]
        deal(deck, players)