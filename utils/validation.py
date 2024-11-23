# utils/validation.py
from typing import Dict, Any
from game.rules import Rules

def validate_move(data: Dict[str, Any], game_state: Dict[str, Any]) -> bool:
    """Валидация хода игрока"""
    if not all(key in data for key in ['card_index', 'position']):
        return False
        
    if data['position'] not in ['top', 'middle', 'bottom']:
        return False
        
    if not (0 <= data['card_index'] < len(game_state['player'].current_cards)):
        return False
        
    # Проверка правил размещения карт
    return Rules.validate_placement(
        game_state['player'].hand['top'],
        game_state['player'].hand['middle'],
        game_state['player'].hand['bottom']
    )

def validate_game_state(game_state: Dict[str, Any]) -> bool:
    """Валидация состояния игры"""
    required_keys = ['player', 'ai', 'deck', 'street']
    return all(key in game_state for key in required_keys)
