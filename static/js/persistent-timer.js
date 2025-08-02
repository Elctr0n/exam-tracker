/**
 * ExamX Persistent Timer System
 * Maintains timer state across all tabs and pages
 */

class PersistentTimer {
    constructor() {
        this.isRunning = false;
        this.startTime = null;
        this.elapsedTime = 0;
        this.timerInterval = null;
        
        // DOM elements
        this.timerDisplay = null;
        this.playBtn = null;
        this.pauseBtn = null;
        this.stopBtn = null;
        
        // Storage keys
        this.STORAGE_KEYS = {
            isRunning: 'examx_timer_running',
            startTime: 'examx_timer_start',
            elapsedTime: 'examx_timer_elapsed',
            todayTime: 'examx_today_time',
            lastDate: 'examx_last_date'
        };
        
        this.init();
    }
    
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupTimer());
        } else {
            this.setupTimer();
        }
        
        // Listen for storage changes (cross-tab synchronization)
        window.addEventListener('storage', (e) => this.handleStorageChange(e));
        
        // Save timer state before page unload
        window.addEventListener('beforeunload', () => this.saveTimerState());
    }
    
    setupTimer() {
        // Find timer elements
        this.timerDisplay = document.getElementById('timerDisplay');
        this.playBtn = document.getElementById('playBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.stopBtn = document.querySelector('.timer-btn.stop');
        
        // Debug logging
        console.log('Timer elements found:', {
            timerDisplay: !!this.timerDisplay,
            playBtn: !!this.playBtn,
            pauseBtn: !!this.pauseBtn,
            stopBtn: !!this.stopBtn
        });
        
        if (!this.timerDisplay) return;
        
        // Restore timer state from localStorage
        this.restoreTimerState();
        
        // Setup event listeners
        if (this.playBtn) {
            this.playBtn.addEventListener('click', () => this.startTimer());
        }
        if (this.pauseBtn) {
            this.pauseBtn.addEventListener('click', () => this.pauseTimer());
        }
        if (this.stopBtn) {
            this.stopBtn.addEventListener('click', () => this.resetTimer());
        }
        
        // Update display
        this.updateDisplay();
        
        // Start interval if timer was running
        if (this.isRunning) {
            this.startInterval();
        }
    }
    
    startTimer() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.startTime = Date.now() - (this.elapsedTime * 1000);
        
        this.startInterval();
        this.updateButtons();
        this.saveTimerState();
        
        // Broadcast to other tabs
        this.broadcastTimerState();
    }
    
    pauseTimer() {
        if (!this.isRunning) return;
        
        this.isRunning = false;
        this.elapsedTime += Math.floor((Date.now() - this.startTime) / 1000);
        
        this.stopInterval();
        this.updateButtons();
        this.saveTimerState();
        
        // Broadcast to other tabs
        this.broadcastTimerState();
    }
    
    resetTimer() {
        this.isRunning = false;
        this.elapsedTime = 0;
        this.startTime = null;
        
        this.stopInterval();
        this.updateDisplay();
        this.updateButtons();
        this.saveTimerState();
        
        // Broadcast to other tabs
        this.broadcastTimerState();
    }
    
    startInterval() {
        this.stopInterval(); // Clear any existing interval
        this.timerInterval = setInterval(() => {
            this.updateDisplay();
        }, 1000);
    }
    
    stopInterval() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }
    
    updateDisplay() {
        if (!this.timerDisplay) return;
        
        let currentElapsed = this.elapsedTime;
        if (this.isRunning && this.startTime) {
            currentElapsed += Math.floor((Date.now() - this.startTime) / 1000);
        }
        
        const hours = Math.floor(currentElapsed / 3600);
        const minutes = Math.floor((currentElapsed % 3600) / 60);
        const seconds = currentElapsed % 60;
        
        this.timerDisplay.textContent = 
            `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // Update today's time if element exists
        const todayTimeElement = document.getElementById('todayTime');
        if (todayTimeElement) {
            const todayMinutes = Math.floor(currentElapsed / 60);
            const todayHours = Math.floor(todayMinutes / 60);
            const remainingMinutes = todayMinutes % 60;
            todayTimeElement.textContent = `${todayHours}h ${remainingMinutes}m`;
        }
    }
    
    updateButtons() {
        if (this.playBtn && this.pauseBtn) {
            if (this.isRunning) {
                this.playBtn.style.display = 'none';
                this.pauseBtn.style.display = 'flex';
            } else {
                this.playBtn.style.display = 'flex';
                this.pauseBtn.style.display = 'none';
            }
        }
    }
    
    saveTimerState() {
        localStorage.setItem(this.STORAGE_KEYS.isRunning, this.isRunning.toString());
        localStorage.setItem(this.STORAGE_KEYS.startTime, this.startTime?.toString() || '');
        localStorage.setItem(this.STORAGE_KEYS.elapsedTime, this.elapsedTime.toString());
        localStorage.setItem(this.STORAGE_KEYS.lastDate, new Date().toDateString());
    }
    
    restoreTimerState() {
        const savedRunning = localStorage.getItem(this.STORAGE_KEYS.isRunning) === 'true';
        const savedStartTime = localStorage.getItem(this.STORAGE_KEYS.startTime);
        const savedElapsed = parseInt(localStorage.getItem(this.STORAGE_KEYS.elapsedTime) || '0');
        const lastDate = localStorage.getItem(this.STORAGE_KEYS.lastDate);
        
        // Reset timer if it's a new day
        const today = new Date().toDateString();
        if (lastDate !== today) {
            this.resetTimer();
            return;
        }
        
        this.isRunning = savedRunning;
        this.elapsedTime = savedElapsed;
        
        if (savedStartTime && savedRunning) {
            this.startTime = parseInt(savedStartTime);
            // Adjust for time passed while page was closed
            const timePassed = Math.floor((Date.now() - this.startTime) / 1000);
            this.elapsedTime = Math.max(0, timePassed);
        }
        
        this.updateButtons();
    }
    
    broadcastTimerState() {
        // Use localStorage to communicate with other tabs
        localStorage.setItem('examx_timer_broadcast', JSON.stringify({
            isRunning: this.isRunning,
            startTime: this.startTime,
            elapsedTime: this.elapsedTime,
            timestamp: Date.now()
        }));
    }
    
    handleStorageChange(e) {
        if (e.key === 'examx_timer_broadcast' && e.newValue) {
            const data = JSON.parse(e.newValue);
            
            // Only update if the broadcast is recent (within 2 seconds)
            if (Date.now() - data.timestamp < 2000) {
                this.isRunning = data.isRunning;
                this.startTime = data.startTime;
                this.elapsedTime = data.elapsedTime;
                
                if (this.isRunning) {
                    this.startInterval();
                } else {
                    this.stopInterval();
                }
                
                this.updateDisplay();
                this.updateButtons();
            }
        }
    }
    
    // Public methods for external use
    getCurrentTime() {
        let currentElapsed = this.elapsedTime;
        if (this.isRunning && this.startTime) {
            currentElapsed += Math.floor((Date.now() - this.startTime) / 1000);
        }
        return currentElapsed;
    }
    
    getTodayStats() {
        const totalSeconds = this.getCurrentTime();
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        
        return {
            totalSeconds,
            hours,
            minutes,
            formatted: `${hours}h ${minutes}m`
        };
    }
}

// Initialize the persistent timer when script loads
window.examxTimer = new PersistentTimer();

// Expose global functions for backward compatibility
window.startTimer = () => window.examxTimer.startTimer();
window.pauseTimer = () => window.examxTimer.pauseTimer();
window.resetTimer = () => window.examxTimer.resetTimer();
