// static/js/cards.js
class Card {
    constructor(rank, suit) {
        this.rank = rank;
        this.suit = suit;
        this.element = this.createElement();
    }

    createElement() {
        const card = document.createElement('div');
        card.className = 'card';
        card.dataset.rank = this.rank;
        card.dataset.suit = this.suit;
        
        const svg = this.createSVG();
        card.appendChild(svg);
        
        this.setupDragAndTouch(card);
        return card;
    }

    // static/js/cards.js (продолжение)
    createSVG() {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('viewBox', '0 0 100 140');
        svg.innerHTML = `
            <rect width="100" height="140" rx="10" ry="10" fill="white" stroke="black"/>
            <text x="50" y="40" text-anchor="middle" font-size="20" fill="${this.getColor()}">${this.rank}</text>
            <text x="50" y="90" text-anchor="middle" font-size="40" fill="${this.getColor()}">${this.getSuitSymbol()}</text>
        `;
        return svg;
    }

    getColor() {
        return ['hearts', 'diamonds'].includes(this.suit) ? 'red' : 'black';
    }

    getSuitSymbol() {
        const symbols = {
            'hearts': '♥',
            'diamonds': '♦',
            'clubs': '♣',
            'spades': '♠'
        };
        return symbols[this.suit];
    }

    setupDragAndTouch(element) {
        element.draggable = true;
        
        // Drag events
        element.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', `${this.rank}-${this.suit}`);
            element.classList.add('dragging');
        });

        element.addEventListener('dragend', () => {
            element.classList.remove('dragging');
        });

        // Touch events
        let startX, startY;
        
        element.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            element.classList.add('dragging');
        });

        element.addEventListener('touchmove', (e) => {
            e.preventDefault();
            const touch = e.touches[0];
            const moveX = touch.clientX - startX;
            const moveY = touch.clientY - startY;
            
            element.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });

        element.addEventListener('touchend', (e) => {
            element.classList.remove('dragging');
            element.style.transform = '';
            
            const touch = e.changedTouches[0];
            const target = document.elementFromPoint(touch.clientX, touch.clientY);
            
            if (target && target.classList.contains('card-slot')) {
                Game.handleCardPlacement(this, target);
            }
        });
    }
}
