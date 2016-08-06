from lora import Color, Value, Card, PlayerError
from lora import move_card, player_put_card, full_deck, deal

class GameBase():
    def __init__(self, players, starting_player):
        self.players = players
        self.starting_player = starting_player
        self.current_player = self.starting_player

        self.pile = []

    def initgame(self):
        for player in self.players:
            player.hand = []
            player.pile = []

        self.pile = []

        deck = full_deck()
        deal(deck, self.players)

    def reordered_players(self):
        current_index = self.players.index(self.current_player)
        for i in range(4):
            yield self.players[(current_index + i) % 4]


class StychyBase(GameBase):
    def game(self):
        while(all(player.hand for player in self.players)):
            yield from self.stych()


    def stych(self):
        self.current_player = self.starting_player

        for player in self.reordered_players():
            card = yield player, self.pile
            #card = player.play_card(self.pile)
            if not self._is_card_valid(card, player):
                raise PlayerError("Invalid card chosen")
            player_put_card(card, player, self.pile)

        trumph = self.pile[0].color

        take_card    = max((card for card in self.pile if card.color == trumph), key=lambda c: c.value.value[0])
        taker_player = take_card.owner

        taker_player.pile.extend(self.pile)
        self.pile = []

        self.current_player = taker_player

    def _is_card_valid(self, chosen_card, player):
        if chosen_card not in player.hand:
            return False

        if not self.pile:
            return True

        trumph = self.pile[0].color
        return trumph == chosen_card.color or all(handcard.color != trumph for handcard in player.hand)

    def invert_if_durch(results):
        if sum(results == 0 for result in results) == len(results) - 1:
            maximum = max(results)
            return [maximum - result for result in results]
        else:
            return results

    def evaluate(self):
        raise NotImplementedError("You cannot play this game")

class Stychy(StychyBase):

    def evaluate(self):
        results = [len(player.pile) / 4 for player in players]
        return self.invert_if_durch(results)

class Cervene(StychyBase):
    def evaluate(self):
        results = [sum(card.color == Color.cerven for card in player.hand) for player in players]
        return self.invert_if_durch(results)

class Horniky(StychyBase):
    def evaluate(self):
        return [2 * sum(card.value == Value.hornik for card in player.hand) for player in players]

class CervenyKral(StychyBase):
    def evaluate(self):
        ck = Card(Color.cerven, Value.kral)
        return [8 * sum(card == ck for card in player.hand) for player in players]

class ZaludnyDolnik(StychyBase):
    def evaluate(self):
        zd = Card(Color.zalud, Value.dolnik)
        return [8 * sum(card == zd for card in player.hand) for player in players]

class PrvyAPosledny(StychyBase):
    def evaluate(self):
        return [8*(self.p1 == player) + 8*(self.p2 == player) for player in self.players]

    def game(self):
        self.stych()
        self.p1 = self.current_player

        while all(player.hand for player in self.players):
            self.stych()

        self.p2 = self.current_player

class MalaLora(GameBase):
    
    def game(self):
        while all(player.hand for player in self.players):
            yield from self.stych()

    def stych(self):
        current_card = yield player, self.pile        
        #current_card = self.current_player.play_card(self.pile)
        self.player_put_card(current_card, self.current_player, self.pile)
        last_put_card = current_card

        for i in range(4):
            for player in self.reordered_players():
                while current_card in player.hand:
                    self.player_put_card(current_card, player, self.pile)
                    if current_card != last_put_card:
                        last_put_card = current_card
            current_card = current_card.next_card()

        self.current_player = last_put_card.owner

    def evaluate(self):
        return [len(player.hand) for player in self.players]

    def players_having_card(self, card):
        return [player for player in self.players if card in player.hand]

class VelkaLora(GameBase):
    def __init__(self, players, starting_player):
        super().__init__(players, starting_player)

        self.piles = {color: list() for color in Color}

    def initgame(self):
        super().initgame()
        self.piles = {color: list() for color in Color}

    def game(self):
        while True:
            for player in self.reordered_players():
                #card = player.play_card(self.pile)
                card = yield player, self.piles
                if not self._is_card_valid(card, player):
                    raise PlayerError("Invalid card chosen")
                self.player_put_card(card, player, self.piles[card.color])

                if not player.hand:
                    break
            else:
                continue
            break


    def _is_card_valid(self, chosen_card, player):
        if chosen_card not in player.hand:
            return False

        # is this card a the next-value card for some pile?        
        for color, pile in self.piles.items:
            if chosen_card == pile[-1].next_card():
                return True
        else:
            # is the player doesn't have anything to put, he must choose None
            return chosen_card is None

    def evaluate(self):
        return [2 * len(player.hand) - 1 if player.hand else 0 for player in self.players]
