// static/js/animations.js
class Animations {
    static async showScoring(scores) {
        const positions = ['top', 'middle', 'bottom'];
        const delays = [0, 500, 1000];
        
        for (let i = 0; i < positions.length; i++) {
            const position = positions[i];
            await this.animateScore(position, scores[position], delays[i]);
        }
        
        // Анимация общего счета
        await this.animateTotalScore(scores.total);
    }

    static animateScore(position, score, delay) {
        return new Promise(resolve => {
            setTimeout(() => {
                const row = document.querySelector(`.player-table .${position}-row`);
                const scoreElement = document.createElement('div');
                scoreElement.className = 'score-animation';
                scoreElement.textContent = score > 0 ? `+${score}` : score;
                
                row.appendChild(scoreElement);
                
                // Trigger animation
                requestAnimationFrame(() => {
                    scoreElement.classList.add('show');
                });
                
                setTimeout(() => {
                    scoreElement.remove();
                    resolve();
                }, 2000);
            }, delay);
        });
    }

    static animateTotalScore(total) {
        return new Promise(resolve => {
            const container = document.createElement('div');
            container.className = 'total-score-animation';
            container.textContent = `Итого: ${total}`;
            
            document.querySelector('.game-container').appendChild(container);
            
            requestAnimationFrame(() => {
                container.classList.add('show');
            });
            
            setTimeout(() => {
                container.classList.add('fade-out');
                setTimeout(() => {
                    container.remove();
                    resolve();
                }, 500);
            }, 3000);
        });
    }

    static cardPlacementAnimation(card, targetSlot) {
        const cardRect = card.getBoundingClientRect();
        const targetRect = targetSlot.getBoundingClientRect();
        
        const deltaX = targetRect.left - cardRect.left;
        const deltaY = targetRect.top - cardRect.top;
        
        card.style.transition = 'transform 0.3s ease';
        card.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        
        return new Promise(resolve => {
            card.addEventListener('transitionend', () => {
                card.style.transition = '';
                card.style.transform = '';
                resolve();
            }, { once: true });
        });
    }
}
