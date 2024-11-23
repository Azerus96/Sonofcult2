# ai/strategy.py
from typing import Dict, List, Tuple
from game.rules import Rules
from game.scoring import Scoring

class Strategy:
    def __init__(self):
        self.rules = Rules()
        self.scoring = Scoring()
        
    def evaluate_move(self, hand: Dict[str, List['Card']], 
                     available_cards: List['Card']) -> Tuple[str, 'Card']:
        """Оценивает лучший ход для текущего состояния"""
        best_score = float('-inf')
        best_move = None
        best_position = None
        
        for card in available_cards:
            for position in ['top', 'middle', 'bottom']:
                if len(hand[position]) >= self.rules.MAX_CARDS[position]:
                    continue
                    
                # Пробуем разместить карту
                temp_hand = self._copy_hand(hand)
                temp_hand[position].append(card)
                
                if self.rules.validate_hand(temp_hand):
                    score = self._evaluate_position(temp_hand)
                    if score > best_score:
                        best_score = score
                        best_move = card
                        best_position = position
                        
        return best_position, best_move
        
    def _copy_hand(self, hand: Dict[str, List['Card']]) -> Dict[str, List['Card']]:
        """Создает копию руки"""
        return {
            position: cards.copy() 
            for position, cards in hand.items()
        }
        
    def _evaluate_position(self, hand: Dict[str, List['Card']]) -> float:
        """Оценивает силу руки"""
        score = 0
        for position in hand:
            line_strength = self.rules.evaluate_line(hand[position])
            score += line_strength
            
            # Учитываем бонусы
            bonus = self.scoring.get_line_bonus(
                hand[position], 
                position, 
                line_strength
            )
            score += bonus
            
        return score
