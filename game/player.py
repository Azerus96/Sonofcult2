# game/player.py
from typing import Dict, List
from .constants import MAX_CARDS
from .rules import Rules

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = {
            'top': [],
            'middle': [],
            'bottom': []
        }
        self.score = 0
        self.current_cards = []
        
    def receive_cards(self, cards: List['Card']):
        self.current_cards.extend(cards)
        
    def place_card(self, card: 'Card', position: str) -> bool:
        if card not in self.current_cards:
            return False
            
        if len(self.hand[position]) >= MAX_CARDS[position]:
            return False
            
        self.hand[position].append(card)
        self.current_cards.remove(card)
        return True
        
    def validate_placement(self) -> bool:
        return Rules.validate_hand(self.hand)
        
    def clear_hand(self):
        self.hand = {
            'top': [],
            'middle': [],
            'bottom': []
        }
        self.current_cards = []
