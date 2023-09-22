from card import PathCard, ActionCard
import random

class Deck():
    def __init__(self):
        self._deck = []
        self._initialise_deck()
        self.shuffle()

    
    def _initialise_deck(self):
        for i in range(4):
            self._deck.append(PathCard.vertical_tunnel())
        
        for i in range(5):
            self._deck.append(PathCard.vertical_junction())
        
        for i in range(5):
            self._deck.append(PathCard.cross_road())
        
        for i in range(5):
            self._deck.append(PathCard.horizontal_junction())

        for i in range(3):
            self._deck.append(PathCard.horizontal_tunnel())
        
        for i in range(4):
            self._deck.append(PathCard.turn())
        
        for i in range(5):
            self._deck.append(PathCard.reversed_turn())
        
        self._deck.append(PathCard.dead_end(['south']))
        self._deck.append(PathCard.dead_end(['north','south']))
        self._deck.append(PathCard.dead_end(['north','east','south']))
        self._deck.append(PathCard.dead_end(['north','east','south','west']))
        self._deck.append(PathCard.dead_end(['west', 'north', 'east']))
        self._deck.append(PathCard.dead_end(['west', 'east']))
        self._deck.append(PathCard.dead_end(['south','east']))
        self._deck.append(PathCard.dead_end(['south','west']))
        self._deck.append(PathCard.dead_end(['west']))

        for i in range(6):
            self._deck.append(ActionCard('map'))
        
        for i in range(9):
            self._deck.append(ActionCard('sabotage'))
        
        for i in range(9):
            self._deck.append(ActionCard('mend'))
        
        for i in range(3):
            self._deck.append(ActionCard('dynamite'))

    def shuffle(self):
        random.shuffle(self._deck)

    def draw(self, num_cards=1):
        if len(self._deck) < num_cards:
            num_cards = len(self._deck)
            
        drawn_cards = [self._deck.pop() for _ in range(num_cards)]
        return drawn_cards if num_cards > 1 else (drawn_cards[0] if drawn_cards else None)

    # def distribute_cards(self, players):
    #     # print(f"Deck before distribution: {self._deck}")
    #     for player in players:
    #         player._sensors['hand-sensor']['value'] = self._deck[:4]
    #         self._deck = self._deck[4:]
    #         # print(f"Cards distributed to {player}: {player._sensors['hand-sensor']['value']}")
    #         # print(f"Deck after distribution: {self._deck}")
        

    def is_empty(self):
        return len(self._deck) == 0
    
    def get_deck(self):
        return self._deck
    
    def __str__(self):
        # Return a string representation of the card
        
        return f"Card: {self.attribute}"

