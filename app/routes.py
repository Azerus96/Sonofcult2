# app/routes.py
from flask import Blueprint, render_template, jsonify, request, session
from game.deck import Deck
from game.player import Player
from game.scoring import Scoring
from ai.mccfr import MCCFRAgent
from ai.progress import ProgressManager
from utils.validation import validate_move
from config import Config

bp = Blueprint('game', __name__)

@bp.before_request
def before_request():
    if 'game_state' not in session:
        session['game_state'] = init_game_state()

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/start', methods=['POST'])
def start_game():
    try:
        game_state = init_game_state()
        session['game_state'] = game_state
        
        # Раздача начальных карт
        deck = Deck()
        player_cards = deck.deal(5)
        ai_cards = deck.deal(5)
        
        game_state['deck'] = deck
        game_state['player'].receive_cards(player_cards)
        game_state['ai'].receive_cards(ai_cards)
        
        return jsonify({
            'status': 'success',
            'player_cards': [card.to_dict() for card in player_cards],
            'ai_cards': [card.to_dict() for card in ai_cards],
            'street': 1
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/api/move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()
        game_state = session['game_state']
        
        if not validate_move(data, game_state):
            return jsonify({
                'status': 'error',
                'message': 'Invalid move'
            }), 400
            
        # Применяем ход игрока
        card = game_state['player'].current_cards[data['card_index']]
        game_state['player'].place_card(card, data['position'])
        
        # Ход ИИ
        ai_move = game_state['ai_agent'].get_best_action(game_state)
        game_state['ai'].apply_move(ai_move)
        
        # Проверяем завершение улицы
        if is_street_complete(game_state):
            next_street = deal_next_street(game_state)
            
        session['game_state'] = game_state
        
        return jsonify({
            'status': 'success',
            'game_state': serialize_game_state(game_state),
            'next_street': next_street if 'next_street' in locals() else None
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/api/score', methods=['GET'])
def get_score():
    try:
        game_state = session['game_state']
        scoring = Scoring()
        
        scores = scoring.calculate_game_score(
            game_state['player'].hand,
            game_state['ai'].hand
        )
        
        return jsonify({
            'status': 'success',
            'scores': scores
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def init_game_state():
    """Инициализация состояния игры"""
    return {
        'player': Player('Player'),
        'ai': Player('AI'),
        'ai_agent': MCCFRAgent(),
        'deck': None,
        'street': 1,
        'progress_manager': ProgressManager(Config.AI_PROGRESS_TOKEN)
    }

def is_street_complete(game_state):
    """Проверка завершения текущей улицы"""
    player_complete = len(game_state['player'].current_cards) == 0
    ai_complete = len(game_state['ai'].current_cards) == 0
    return player_complete and ai_complete

def deal_next_street(game_state):
    """Раздача карт для следующей улицы"""
    if game_state['street'] >= 5:
        return None
        
    game_state['street'] += 1
    player_cards = game_state['deck'].deal(3)
    ai_cards = game_state['deck'].deal(3)
    
    game_state['player'].receive_cards(player_cards)
    game_state['ai'].receive_cards(ai_cards)
    
    return {
        'street': game_state['street'],
        'player_cards': [card.to_dict() for card in player_cards],
        'ai_cards': [card.to_dict() for card in ai_cards]
    }

def serialize_game_state(game_state):
    """Сериализация состояния игры для отправки клиенту"""
    return {
        'player_hand': {
            pos: [card.to_dict() for card in cards]
            for pos, cards in game_state['player'].hand.items()
        },
        'ai_hand': {
            pos: [card.to_dict() for card in cards]
            for pos, cards in game_state['ai'].hand.items()
        },
        'street': game_state['street']
    }
