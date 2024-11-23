# game/constants.py
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

HAND_RANKINGS = {
    'high_card': 1,
    'pair': 2,
    'two_pair': 3,
    'three_kind': 4,
    'straight': 5,
    'flush': 6,
    'full_house': 7,
    'four_kind': 8,
    'straight_flush': 9,
    'royal_flush': 10
}

BONUSES = {
    'top': {
        'pair': {'QQ': 1, 'KK': 2, 'AA': 3},
        'three_kind': {'222': 4, '333': 5, '444': 6, '555': 7,
                      '666': 8, '777': 9, '888': 10, '999': 11,
                      'TTT': 12, 'JJJ': 13, 'QQQ': 14, 'KKK': 15,
                      'AAA': 16}
    },
    'middle': {
        'straight': 4,
        'flush': 8,
        'full_house': 12,
        'four_kind': 20,
        'straight_flush': 30,
        'royal_flush': 50
    },
    'bottom': {
        'straight': 2,
        'flush': 4,
        'full_house': 6,
        'four_kind': 10,
        'straight_flush': 15,
        'royal_flush': 25
    }
}
