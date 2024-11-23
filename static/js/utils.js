// static/js/utils.js
class Utils {
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    static saveGameState(state) {
        localStorage.setItem('gameState', JSON.stringify(state));
    }

    static loadGameState() {
        const state = localStorage.getItem('gameState');
        return state ? JSON.parse(state) : null;
    }

    static clearGameState() {
        localStorage.removeItem('gameState');
    }

    static validateCardPlacement(card, slot, gameState) {
        const position = slot.closest('.row').dataset.position;
        const currentCards = gameState.getCurrentPlacements()[position];
        
        // Проверка максимального количества карт
        const maxCards = position === 'top' ? 3 : 5;
        if (currentCards.length >= maxCards) {
            return false;
        }
        
        return true;
    }

    static getCardValue(rank) {
        const values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        };
        return values[rank] || 0;
    }

    static compareCards(card1, card2) {
        const value1 = this.getCardValue(card1.rank);
        const value2 = this.getCardValue(card2.rank);
        return value1 - value2;
    }

    static handleTouchMove(event) {
        if (event.touches.length !== 1) return;
        
        event.preventDefault();
        const touch = event.touches[0];
        const element = document.elementFromPoint(touch.clientX, touch.clientY);
        
        if (element && element.classList.contains('card-slot')) {
            element.classList.add('highlight');
        }
    }

    static async fetchWithTimeout(resource, options = {}) {
        const { timeout = 5000 } = options;
        
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout);
        
        try {
            const response = await fetch(resource, {
                ...options,
                signal: controller.signal
            });
            clearTimeout(id);
            return response;
        } catch (error) {
            clearTimeout(id);
            throw error;
        }
    }

    static showError(message) {
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.textContent = message;
        
        document.body.appendChild(errorElement);
        
        setTimeout(() => {
            errorElement.classList.add('show');
            setTimeout(() => {
                errorElement.classList.remove('show');
                setTimeout(() => {
                    errorElement.remove();
                }, 300);
            }, 3000);
        }, 100);
    }
}
