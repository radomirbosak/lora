#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lora import Card, Player, deal, full_deck, deck_string
from games import Stychy

def main():
    deck = full_deck()

    players = [Player('Player {}'.format(i)) for i in range(4)]
    deal(deck, players)

    # let's play stychy
    stychy = Stychy(players, players[0])
    stychy.initgame()

    # obtain the game generator
    game = stychy.game()
    player, pile = game.send(None)

    while 1:
        prompt = "{}: ".format(player.name)
        
        print_game_state(stychy, player)
        card = Card.from_string(input(prompt))
        player, pile = game.send(card)

def print_game_state(game, player):
    game_name = "Stychy"
    hand_line = "{player}'s hand: {hand}".format(player=player.name, hand=deck_string(player.hand))
    pile_line = "Pile: {}".format(deck_string(game.pile))
    
    print(game_name)
    print(hand_line)
    print(pile_line)




if __name__ == '__main__':
    main()