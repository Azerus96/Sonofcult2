# ai/mccfr.py
from typing import Dict, List, Tuple
import numpy as np
from game.rules import Rules
from game.scoring import Scoring

class MCCFRAgent:
    def __init__(self, iterations: int = 1000):
        self.iterations = iterations
        self.rules = Rules()
        self.scoring = Scoring()
        self.regret_sum = {}
        self.strategy_sum = {}
        self.rules = Rules()
        
    def get_info_set(self, state: Dict) -> str:
        """Преобразует текущее состояние игры в строковый ключ"""
        return f"{state['hand']}_{state['available_cards']}"
        
    def get_strategy(self, info_set: str) -> Dict[str, float]:
        """Получает стратегию для текущего информационного набора"""
        if info_set not in self.regret_sum:
            return self.get_initial_strategy()
            
        regrets = self.regret_sum[info_set]
        positive_regrets = {a: max(r, 0) for a, r in regrets.items()}
        regret_sum = sum(positive_regrets.values())
        
        if regret_sum > 0:
            strategy = {a: r/regret_sum for a, r in positive_regrets.items()}
        else:
            strategy = self.get_initial_strategy()
            
        return strategy
        
    def get_initial_strategy(self) -> Dict[str, float]:
        """Возвращает начальную равномерную стратегию"""
        positions = ['top', 'middle', 'bottom']
        return {pos: 1.0/len(positions) for pos in positions}
        
    def train(self, initial_state: Dict):
        """Обучение агента через MCCFR"""
        for _ in range(self.iterations):
            self._cfr_iteration(initial_state)
            
    def _cfr_iteration(self, state: Dict, reach_prob: float = 1.0):
        """Одна итерация CFR"""
        info_set = self.get_info_set(state)
        strategy = self.get_strategy(info_set)
        
        # Вычисление значений для каждого действия
        action_values = {}
        for action in strategy:
            new_state = self.apply_action(state, action)
            action_values[action] = -self._cfr_recursion(new_state, reach_prob * strategy[action])
            
        # Обновление сожалений и стратегии
        value = 0
        for action in strategy:
            value += strategy[action] * action_values[action]
            regret = action_values[action] - value
            
            if info_set not in self.regret_sum:
                self.regret_sum[info_set] = {}
            if action not in self.regret_sum[info_set]:
                self.regret_sum[info_set][action] = 0
                
            self.regret_sum[info_set][action] += reach_prob * regret
            
        return value
        
    def _cfr_recursion(self, state: Dict, reach_prob: float) -> float:
        """Рекурсивная часть CFR"""
        if self.is_terminal(state):
            return self.get_utility(state)
            
        info_set = self.get_info_set(state)
        strategy = self.get_strategy(info_set)
        
        # Рекурсивный вызов для каждого действия
        value = 0
        for action, prob in strategy.items():
            new_state = self.apply_action(state, action)
            action_value = self._cfr_recursion(new_state, reach_prob * prob)
            value += prob * action_value
            
        return value
        
    def apply_action(self, state: Dict, action: str) -> Dict:
        """Применяет действие к текущему состоянию"""
        new_state = state.copy()
        # Логика размещения карты в выбранную позицию
        return new_state
        
    def is_terminal(self, state: Dict) -> bool:
        """Проверяет, является ли состояние терминальным"""
        return len(state['available_cards']) == 0
        
    def get_utility(self, state: Dict) -> float:
        """Вычисляет полезность терминального состояния"""
        return self.scoring.calculate_game_score(state['hand'], state['opponent_hand'])['total']
        
    def get_best_action(self, state: Dict) -> str:
        """Выбирает лучшее действие для текущего состояния"""
        info_set = self.get_info_set(state)
        strategy = self.get_strategy(info_set)
        return max(strategy.items(), key=lambda x: x[1])[0]
