# game/rules.py
from typing import List, Dict
from .constants import HAND_RANKINGS

class Rules:
    @staticmethod
    def validate_hand(hand: Dict[str, List['Card']]) -> bool:
        # Проверка количества карт
        if len(hand['top']) != 3 or len(hand['middle']) != 5 or len(hand['bottom']) != 5:
            return False
            
        # Получение силы каждой линии
        top_strength = Rules.evaluate_line(hand['top'])
        middle_strength = Rules.evaluate_line(hand['middle'])
        bottom_strength = Rules.evaluate_line(hand['bottom'])
        
        # Проверка правила возрастания силы комбинаций
        return top_strength <= middle_strength <= bottom_strength
    
    @staticmethod
    def evaluate_line(cards: List['Card']) -> int:
        if not cards:
            return 0
            
        ranks = [card.rank for card in cards]
        suits = [card.suit for card in cards]
        
        # Проверка комбинаций от сильнейшей к слабейшей
        if Rules.is_royal_flush(ranks, suits):
            return HAND_RANKINGS['royal_flush']
        if Rules.is_straight_flush(ranks, suits):
            return HAND_RANKINGS['straight_flush']
        if Rules.is_four_kind(ranks):
            return HAND_RANKINGS['four_kind']
        if Rules.is_full_house(ranks):
            return HAND_RANKINGS['full_house']
        if Rules.is_flush(suits):
            return HAND_RANKINGS['flush']
        if Rules.is_straight(ranks):
            return HAND_RANKINGS['straight']
        if Rules.is_three_kind(ranks):
            return HAND_RANKINGS['three_kind']
        if Rules.is_two_pair(ranks):
            return HAND_RANKINGS['two_pair']
        if Rules.is_pair(ranks):
            return HAND_RANKINGS['pair']
            
        return HAND_RANKINGS['high_card']
    
    @staticmethod
    def is_royal_flush(ranks: List[str], suits: List[str]) -> bool:
        royal_ranks = {'10', 'J', 'Q', 'K', 'A'}
        return len(set(suits)) == 1 and set(ranks) == royal_ranks
    
    @staticmethod
    def is_straight_flush(ranks: List[str], suits: List[str]) -> bool:
        return Rules.is_flush(suits) and Rules.is_straight(ranks)
    
    @staticmethod
    def is_four_kind(ranks: List[str]) -> bool:
        return any(ranks.count(rank) == 4 for rank in set(ranks))
    
    @staticmethod
    def is_full_house(ranks: List[str]) -> bool:
        rank_counts = [ranks.count(rank) for rank in set(ranks)]
        return sorted(rank_counts) == [2, 3]
    
    @staticmethod
    def is_flush(suits: List[str]) -> bool:
        return len(set(suits)) == 1
    
    @staticmethod
    def is_straight(ranks: List[str]) -> bool:
        rank_values = [Rules.get_rank_value(r) for r in ranks]
        rank_values.sort()
        return rank_values == list(range(min(rank_values), max(rank_values) + 1))
    
    @staticmethod
    def is_three_kind(ranks: List[str]) -> bool:
        return any(ranks.count(rank) == 3 for rank in set(ranks))
    
    @staticmethod
    def is_two_pair(ranks: List[str]) -> bool:
        pairs = sum(1 for rank in set(ranks) if ranks.count(rank) == 2)
        return pairs == 2
    
    @staticmethod
    def is_pair(ranks: List[str]) -> bool:
        return any(ranks.count(rank) == 2 for rank in set(ranks))
    
    @staticmethod
    def get_rank_value(rank: str) -> int:
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                 '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return values[rank]
