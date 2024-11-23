# game/deck.py
from typing import List, Tuple
import random
from .constants import SUITS, RANKS

class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        
    def __repr__(self):
        return f"{self.rank}{self.suit}"
        
    def to_dict(self):
        return {
            'rank': self.rank,
            'suit': self.suit
        }

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        self.used_cards = set()
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self, count: int) -> List[Card]:
        available = [c for c in self.cards if c not in self.used_cards]
        if len(available) < count:
            raise ValueError("Not enough cards in deck")
            
        dealt = random.sample(available, count)
        self.used_cards.update(dealt)
        return dealt
        
    def reset(self):
        self.used_cards.clear()
