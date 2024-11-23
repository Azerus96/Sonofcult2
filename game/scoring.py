# game/scoring.py
from typing import Dict, List
from .constants import BONUSES
from .rules import Rules

class Scoring:
    def __init__(self):
        self.rules = Rules()
    
    def calculate_game_score(self, player_hand: Dict[str, List['Card']], 
                           opponent_hand: Dict[str, List['Card']]) -> Dict[str, int]:
        if not self.rules.validate_hand(player_hand) or not self.rules.validate_hand(opponent_hand):
            return {'total': 0, 'top': 0, 'middle': 0, 'bottom': 0}
        
        scores = {
            'top': self.compare_lines(player_hand['top'], opponent_hand['top'], 'top'),
            'middle': self.compare_lines(player_hand['middle'], opponent_hand['middle'], 'middle'),
            'bottom': self.compare_lines(player_hand['bottom'], opponent_hand['bottom'], 'bottom')
        }
        
        # Добавление бонуса за победу во всех линиях
        if all(score > 0 for score in scores.values()):
            scores['total'] = sum(scores.values()) + 3
        else:
            scores['total'] = sum(scores.values())
            
        # Добавление бонусов за специальные комбинации
        bonus_scores = self.calculate_bonuses(player_hand)
        for position in scores:
            if position in bonus_scores:
                scores[position] += bonus_scores[position]
                
        return scores
    
    def compare_lines(self, player_line: List['Card'], opponent_line: List['Card'], 
                     position: str) -> int:
        player_strength = self.rules.evaluate_line(player_line)
        opponent_strength = self.rules.evaluate_line(opponent_line)
        
        if player_strength > opponent_strength:
            return 1
        elif player_strength < opponent_strength:
            return -1
        else:
            # При равной силе комбинаций сравниваем старшие карты
            return self.compare_high_cards(player_line, opponent_line)
    
    def calculate_bonuses(self, hand: Dict[str, List['Card']]) -> Dict[str, int]:
        bonuses = {'top': 0, 'middle': 0, 'bottom': 0}
        
        for position in hand:
            line_strength = self.rules.evaluate_line(hand[position])
            line_bonus = self.get_line_bonus(hand[position], position, line_strength)
            bonuses[position] += line_bonus
            
        return bonuses
    
    def get_line_bonus(self, line: List['Card'], position: str, strength: int) -> int:
        if position not in BONUSES:
            return 0
            
        line_bonuses = BONUSES[position]
        hand_type = self.get_hand_type(strength)
        
        if hand_type in line_bonuses:
            if isinstance(line_bonuses[hand_type], dict):
                # Для специальных комбинаций (например, конкретных пар)
                key = ''.join(sorted([card.rank for card in line]))
                return line_bonuses[hand_type].get(key, 0)
            else:
                return line_bonuses[hand_type]
                
        return 0
