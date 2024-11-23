// static/js/game.js
class Game {
    constructor() {
        this.init();
        this.bindEvents();
    }

    init() {
        this.currentStreet = 0;
        this.playerCards = [];
        this.aiCards = [];
        this.startBtn = document.getElementById('startBtn');
        this.okBtn = document.getElementById('okBtn');
        this.currentCardsContainer = document.querySelector('.current-cards');
    }

    bindEvents() {
        this.startBtn.addEventListener('click', () => this.startGame());
        this.okBtn.addEventListener('click', () => this.nextStreet());
        
        // Setup drop zones
        document.querySelectorAll('.card-slot').forEach(slot => {
            slot.addEventListener('dragover', (e) => {
                e.preventDefault();
                slot.classList.add('highlight');
            });

            slot.addEventListener('dragleave', () => {
                slot.classList.remove('highlight');
            });

            slot.addEventListener('drop', (e) => {
                e.preventDefault();
                slot.classList.remove('highlight');
                const cardData = e.dataTransfer.getData('text/plain');
                const [rank, suit] = cardData.split('-');
                this.handleCardPlacement({ rank, suit }, slot);
            });
        });
    }

    async startGame() {
        try {
            const response = await fetch('/api/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const data = await response.json();
            if (data.status === 'success') {
                this.currentStreet = 1;
                this.renderCards(data.player_cards);
                this.renderAICards(data.ai_cards);
                this.startBtn.disabled = true;
                this.okBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error starting game:', error);
        }
    }

    async nextStreet() {
        if (!this.validateCurrentPlacement()) {
            alert('Пожалуйста, разместите все карты корректно');
            return;
        }

        try {
            const response = await fetch('/api/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    street: this.currentStreet,
                    placements: this.getCurrentPlacements()
                })
            });

            const data = await response.json();
            if (data.status === 'success') {
                if (data.next_street) {
                    this.currentStreet = data.next_street.street;
                    this.renderCards(data.next_street.player_cards);
                    this.renderAICards(data.next_street.ai_cards);
                } else {
                    this.endGame();
                }
            }
        } catch (error) {
            console.error('Error making move:', error);
        }
    }

    renderCards(cards) {
        this.currentCardsContainer.innerHTML = '';
        cards.forEach(cardData => {
            const card = new Card(cardData.rank, cardData.suit);
            this.currentCardsContainer.appendChild(card.element);
        });
    }

    renderAICards(cards) {
        const aiSlots = document.querySelectorAll('.ai-table .card-slot');
        cards.forEach((cardData, index) => {
            if (aiSlots[index]) {
                const card = new Card(cardData.rank, cardData.suit);
                aiSlots[index].appendChild(card.element);
            }
        });
    }

    validateCurrentPlacement() {
        // Проверка правильности размещения карт
        const placements = this.getCurrentPlacements();
        return Object.values(placements).every(line => 
            line.length <= (line.position === 'top' ? 3 : 5));
    }

    getCurrentPlacements() {
        const placements = {
            top: [],
            middle: [],
            bottom: []
        };

        document.querySelectorAll('.player-table .card-slot').forEach(slot => {
            const card = slot.querySelector('.card');
            if (card) {
                const position = slot.closest('.row').dataset.position;
                placements[position].push({
                    rank: card.dataset.rank,
                    suit: card.dataset.suit
                });
            }
        });

        return placements;
    }

    async endGame() {
        try {
            const response = await fetch('/api/score');
            const data = await response.json();
            
            if (data.status === 'success') {
                Animations.showScoring(data.scores);
                this.okBtn.disabled = true;
                this.startBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error getting score:', error);
        }
    }

    static handleCardPlacement(card, slot) {
        if (slot.children.length === 0) {
            slot.appendChild(card.element);
            return true;
        }
        return false;
    }
}

// static/js/game.js (продолжение)
document.addEventListener('DOMContentLoaded', () => {
    window.game = new Game();
    
    // Восстановление состояния игры при перезагрузке
    const savedState = localStorage.getItem('gameState');
    if (savedState) {
        const state = JSON.parse(savedState);
        game.restoreState(state);
    }
});
