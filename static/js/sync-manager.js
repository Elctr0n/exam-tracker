/**
 * ExamX Sync Manager
 * Handles all client-server synchronization for user data, settings, and activity
 */

class SyncManager {
    constructor() {
        this.userId = null;
        this.syncInterval = null;
        this.pendingSync = false;
        this.syncQueue = [];
        
        // Initialize sync manager
        this.init();
    }
    
    init() {
        // Get user ID from Firebase auth or localStorage
        this.getUserId();
        
        // Start periodic sync every 30 seconds
        this.startPeriodicSync();
        
        // Sync on page load
        this.syncAllData();
        
        // Sync before page unload
        window.addEventListener('beforeunload', () => {
            this.syncAllData();
        });
        
        // Sync on visibility change (when user switches tabs)
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.syncAllData();
            }
        });
    }
    
    getUserId() {
        // Try to get from Firebase auth first
        if (typeof firebase !== 'undefined' && firebase.auth && firebase.auth().currentUser) {
            this.userId = firebase.auth().currentUser.uid;
        } else {
            // Fallback to localStorage
            const userData = JSON.parse(localStorage.getItem('userData') || '{}');
            this.userId = userData.uid || localStorage.getItem('userId');
        }
        
        console.log('SyncManager initialized for user:', this.userId);
    }
    
    startPeriodicSync() {
        // Sync every 30 seconds
        this.syncInterval = setInterval(() => {
            this.syncAllData();
        }, 30000);
    }
    
    stopPeriodicSync() {
        if (this.syncInterval) {
            clearInterval(this.syncInterval);
            this.syncInterval = null;
        }
    }
    
    async syncAllData() {
        if (!this.userId || this.pendingSync) return;
        
        this.pendingSync = true;
        
        try {
            // Collect all data to sync
            const syncData = {
                user_id: this.userId,
                settings: this.collectUserSettings(),
                progress: this.collectProgressData(),
                timestamp: new Date().toISOString()
            };
            
            // Send to server
            const response = await fetch('/api/user/sync', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(syncData)
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log('✅ Data synced successfully:', result);
                
                // Update local data with server response
                if (result.settings) {
                    this.updateLocalSettings(result.settings);
                }
                
                // Clear sync queue
                this.syncQueue = [];
                
                // Update UI with latest statistics
                if (result.statistics) {
                    this.updateUIStatistics(result.statistics);
                }
            } else {
                console.error('❌ Sync failed:', response.statusText);
            }
        } catch (error) {
            console.error('❌ Sync error:', error);
        } finally {
            this.pendingSync = false;
        }
    }
    
    collectUserSettings() {
        return {
            study_reminders: localStorage.getItem('examx_study_reminders') === 'true',
            dark_mode: localStorage.getItem('examx_dark_mode') === 'true',
            privacy_mode: localStorage.getItem('examx_privacy_mode') === 'true',
            notification_preferences: JSON.parse(localStorage.getItem('examx_notification_preferences') || '{}'),
            theme_preferences: JSON.parse(localStorage.getItem('examx_theme_preferences') || '{}'),
            study_schedule: JSON.parse(localStorage.getItem('examx_study_schedule') || '{}')
        };
    }
    
    collectProgressData() {
        const progressData = {};
        
        // Get all progress data from localStorage
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith('examx_progress_')) {
                const examName = key.replace('examx_progress_', '');
                const progressString = localStorage.getItem(key);
                if (progressString) {
                    try {
                        progressData[examName] = JSON.parse(progressString);
                    } catch (e) {
                        console.warn('Failed to parse progress data for:', examName);
                    }
                }
            }
        }
        
        return progressData;
    }
    
    updateLocalSettings(serverSettings) {
        // Update localStorage with server settings
        localStorage.setItem('examx_study_reminders', serverSettings.study_reminders || false);
        localStorage.setItem('examx_dark_mode', serverSettings.dark_mode || false);
        localStorage.setItem('examx_privacy_mode', serverSettings.privacy_mode || false);
        localStorage.setItem('examx_notification_preferences', JSON.stringify(serverSettings.notification_preferences || {}));
        localStorage.setItem('examx_theme_preferences', JSON.stringify(serverSettings.theme_preferences || {}));
        localStorage.setItem('examx_study_schedule', JSON.stringify(serverSettings.study_schedule || {}));
        
        // Update UI toggles if they exist
        this.updateSettingsToggles(serverSettings);
    }
    
    updateSettingsToggles(settings) {
        const studyRemindersToggle = document.getElementById('studyRemindersToggle');
        const darkModeToggle = document.getElementById('darkModeToggle');
        const privacyModeToggle = document.getElementById('privacyModeToggle');
        
        if (studyRemindersToggle) {
            studyRemindersToggle.checked = settings.study_reminders || false;
        }
        if (darkModeToggle) {
            darkModeToggle.checked = settings.dark_mode || false;
            // Apply dark mode if enabled
            if (settings.dark_mode) {
                document.body.classList.add('dark-mode');
            }
        }
        if (privacyModeToggle) {
            privacyModeToggle.checked = settings.privacy_mode || false;
        }
    }
    
    updateUIStatistics(stats) {
        // Update statistics in UI elements
        const elements = {
            'totalStudyTime': this.formatTime(stats.total_study_time || 0),
            'studyStreak': stats.study_streak || 0,
            'completedTopics': stats.completed_topics || 0,
            'totalExams': stats.total_exams || 0,
            'recentSessions': stats.recent_sessions || 0
        };
        
        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }
    
    formatTime(minutes) {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return `${hours}h ${mins}m`;
    }
    
    async saveUserSettings(settings) {
        if (!this.userId) return false;
        
        try {
            const response = await fetch('/api/user/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.userId,
                    settings: settings
                })
            });
            
            if (response.ok) {
                console.log('✅ Settings saved to server');
                return true;
            } else {
                console.error('❌ Failed to save settings to server');
                return false;
            }
        } catch (error) {
            console.error('❌ Settings save error:', error);
            return false;
        }
    }
    
    async logActivity(activityType, activityData = {}, exam = null, subject = null, topic = null, sessionDuration = 0) {
        if (!this.userId) return false;
        
        try {
            const response = await fetch('/api/user/activity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.userId,
                    activity_type: activityType,
                    activity_data: activityData,
                    exam: exam,
                    subject: subject,
                    topic: topic,
                    session_duration: sessionDuration
                })
            });
            
            if (response.ok) {
                console.log('✅ Activity logged:', activityType);
                return true;
            } else {
                console.error('❌ Failed to log activity');
                return false;
            }
        } catch (error) {
            console.error('❌ Activity log error:', error);
            return false;
        }
    }
    
    async startStudySession(exam, subject = null, topic = null) {
        if (!this.userId) return null;
        
        try {
            const response = await fetch('/api/user/study-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'start',
                    user_id: this.userId,
                    exam: exam,
                    subject: subject,
                    topic: topic
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log('✅ Study session started:', result.session_id);
                return result.session_id;
            } else {
                console.error('❌ Failed to start study session');
                return null;
            }
        } catch (error) {
            console.error('❌ Study session start error:', error);
            return null;
        }
    }
    
    async endStudySession(sessionId, notes = null) {
        if (!this.userId || !sessionId) return null;
        
        try {
            const response = await fetch('/api/user/study-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'end',
                    user_id: this.userId,
                    session_id: sessionId,
                    notes: notes
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log('✅ Study session ended:', result.duration, 'minutes');
                return result.duration;
            } else {
                console.error('❌ Failed to end study session');
                return null;
            }
        } catch (error) {
            console.error('❌ Study session end error:', error);
            return null;
        }
    }
    
    async loadUserSettings() {
        if (!this.userId) return null;
        
        try {
            const response = await fetch(`/api/user/settings?user_id=${this.userId}`);
            
            if (response.ok) {
                const result = await response.json();
                console.log('✅ Settings loaded from server');
                this.updateLocalSettings(result.settings);
                return result.settings;
            } else {
                console.error('❌ Failed to load settings from server');
                return null;
            }
        } catch (error) {
            console.error('❌ Settings load error:', error);
            return null;
        }
    }
    
    // Enhanced timer integration with server sync
    enhanceTimerWithSync() {
        // Override timer methods to include server sync
        if (window.persistentTimer) {
            const originalStart = window.persistentTimer.start.bind(window.persistentTimer);
            const originalStop = window.persistentTimer.stop.bind(window.persistentTimer);
            
            window.persistentTimer.start = () => {
                originalStart();
                // Start study session on server
                this.currentSessionId = this.startStudySession('General Study');
                this.logActivity('timer_started', { timestamp: new Date().toISOString() });
            };
            
            window.persistentTimer.stop = () => {
                const duration = window.persistentTimer.getElapsedTime();
                originalStop();
                // End study session on server
                if (this.currentSessionId) {
                    this.endStudySession(this.currentSessionId);
                    this.currentSessionId = null;
                }
                this.logActivity('timer_stopped', { 
                    duration: duration,
                    timestamp: new Date().toISOString() 
                });
            };
        }
    }
}

// Global sync manager instance
window.syncManager = new SyncManager();

// Initialize enhanced functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Enhance timer with sync capabilities
    window.syncManager.enhanceTimerWithSync();
    
    // Load user settings from server
    window.syncManager.loadUserSettings();
    
    console.log('🔄 ExamX Sync Manager initialized');
});
