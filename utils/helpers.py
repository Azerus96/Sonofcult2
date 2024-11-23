# utils/helpers.py
from typing import Dict, Any
from game.deck import Card

def serialize_game_state(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Сериализация состояния игры для сохранения"""
    return {
        'player_hand': {
            pos: [{'rank': card.rank, 'suit': card.suit} 
                  for card in cards]
            for pos, cards in game_state['player'].hand.items()
        },
        'ai_hand': {
            pos: [{'rank': card.rank, 'suit': card.suit} 
                  for card in cards]
            for pos, cards in game_state['ai'].hand.items()
        },
        'current_street': game_state['street'],
        'deck_state': [{'rank': card.rank, 'suit': card.suit} 
                      for card in game_state['deck'].cards],
        'used_cards': [{'rank': card.rank, 'suit': card.suit} 
                      for card in game_state['deck'].used_cards]
    }

def deserialize_game_state(data: Dict[str, Any]) -> Dict[str, Any]:
    """Десериализация сохраненного состояния игры"""
    from game.player import Player
    from game.deck import Deck
    
    game_state = {
        'player': Player('Player'),
        'ai': Player('AI'),
        'deck': Deck(),
        'street': data['current_street']
    }
    
    # Восстановление состояния колоды
    game_state['deck'].cards = [Card(c['rank'], c['suit']) 
                               for c in data['deck_state']]
    game_state['deck'].used_cards = {Card(c['rank'], c['suit']) 
                                    for c in data['used_cards']}
    
    # Восстановление рук игроков
    for pos, cards in data['player_hand'].items():
        game_state['player'].hand[pos] = [Card(c['rank'], c['suit']) 
                                         for c in cards]
    
    for pos, cards in data['ai_hand'].items():
        game_state['ai'].hand[pos] = [Card(c['rank'], c['suit']) 
                                     for c in cards]
    
    return game_state
