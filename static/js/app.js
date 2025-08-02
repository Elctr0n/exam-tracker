class ExamTracker {
    constructor() {
        this.currentExam = 'jee_mains';
        this.syllabi = {};
        this.userProgress = {};
        this.init();
    }

    async init() {
        await this.loadSyllabi();
        this.setupEventListeners();
        await this.loadExamContent(this.currentExam);
        await this.updateStatsOverview();
        this.hideLoading();
    }

    async loadSyllabi() {
        try {
            const response = await fetch('/api/syllabi');
            this.syllabi = await response.json();
        } catch (error) {
            this.showToast('Error loading syllabi', 'error');
            console.error('Error loading syllabi:', error);
        }
    }

    setupEventListeners() {
        // Tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const exam = e.target.dataset.exam;
                this.switchExam(exam);
            });
        });
    }

    async switchExam(exam) {
        // Update active tab
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-exam="${exam}"]`).classList.add('active');

        this.currentExam = exam;
        await this.loadExamContent(exam);
        await this.updateStatsOverview();
    }

    async loadExamContent(exam) {
        this.showLoading();
        
        try {
            // Load user progress for this exam
            const progressResponse = await fetch(`/api/progress/${exam}`);
            this.userProgress[exam] = await progressResponse.json();

            const examData = this.syllabi[exam];
            if (!examData) {
                throw new Error('Exam data not found');
            }

            const contentHtml = this.generateExamContentHtml(exam, examData);
            document.getElementById('examContent').innerHTML = contentHtml;

            // Setup topic checkboxes
            this.setupTopicCheckboxes(exam);

        } catch (error) {
            this.showToast('Error loading exam content', 'error');
            console.error('Error loading exam content:', error);
        }
        
        this.hideLoading();
    }

    generateExamContentHtml(exam, examData) {
        let html = `<h2 class="exam-title">${examData.name}</h2>`;
        html += '<div class="subjects-grid">';

        for (const [subjectName, subjectData] of Object.entries(examData.subjects)) {
            const subjectProgress = this.calculateSubjectProgress(exam, subjectName, subjectData.topics);
            
            html += `
                <div class="subject-card">
                    <h3 class="subject-title">
                        <i class="fas fa-book"></i>
                        ${subjectName}
                    </h3>
                    <div class="subject-progress">
                        Progress: ${subjectProgress.completed}/${subjectProgress.total} topics (${subjectProgress.percentage}%)
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${subjectProgress.percentage}%"></div>
                        </div>
                    </div>
                    <ul class="topics-list">
            `;

            subjectData.topics.forEach(topic => {
                const isCompleted = this.isTopicCompleted(exam, subjectName, topic);
                const completionDate = this.getTopicCompletionDate(exam, subjectName, topic);
                
                html += `
                    <li class="topic-item ${isCompleted ? 'completed' : ''}">
                        <div class="topic-checkbox ${isCompleted ? 'completed' : ''}" 
                             data-exam="${exam}" 
                             data-subject="${subjectName}" 
                             data-topic="${topic}">
                            ${isCompleted ? '<i class="fas fa-check"></i>' : ''}
                        </div>
                        <span class="topic-name">${topic}</span>
                        ${completionDate ? `<span class="completion-date">${this.formatDate(completionDate)}</span>` : ''}
                    </li>
                `;
            });

            html += '</ul></div>';
        }

        html += '</div>';
        return html;
    }

    setupTopicCheckboxes(exam) {
        document.querySelectorAll('.topic-checkbox').forEach(checkbox => {
            checkbox.addEventListener('click', async (e) => {
                const exam = e.target.dataset.exam;
                const subject = e.target.dataset.subject;
                const topic = e.target.dataset.topic;
                
                const isCompleted = e.target.classList.contains('completed');
                await this.toggleTopic(exam, subject, topic, !isCompleted);
            });
        });
    }

    async toggleTopic(exam, subject, topic, completed) {
        try {
            const response = await fetch('/api/toggle-topic', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    exam,
                    subject,
                    topic,
                    completed
                })
            });

            if (response.ok) {
                // Update UI
                await this.loadExamContent(exam);
                await this.updateStatsOverview();
                
                const message = completed ? 'Topic marked as completed!' : 'Topic marked as incomplete';
                this.showToast(message, 'success');
            } else {
                throw new Error('Failed to update topic');
            }
        } catch (error) {
            this.showToast('Error updating topic', 'error');
            console.error('Error updating topic:', error);
        }
    }

    calculateSubjectProgress(exam, subject, topics) {
        let completed = 0;
        const total = topics.length;

        topics.forEach(topic => {
            if (this.isTopicCompleted(exam, subject, topic)) {
                completed++;
            }
        });

        const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

        return { completed, total, percentage };
    }

    isTopicCompleted(exam, subject, topic) {
        return this.userProgress[exam] && 
               this.userProgress[exam][subject] && 
               this.userProgress[exam][subject][topic] && 
               this.userProgress[exam][subject][topic].completed;
    }

    getTopicCompletionDate(exam, subject, topic) {
        if (this.userProgress[exam] && 
            this.userProgress[exam][subject] && 
            this.userProgress[exam][subject][topic]) {
            return this.userProgress[exam][subject][topic].completed_date;
        }
        return null;
    }

    async updateStatsOverview() {
        const statsHtml = await this.generateStatsHtml();
        document.getElementById('statsOverview').innerHTML = statsHtml;
        
        const summaryHtml = await this.generateProgressSummaryHtml();
        document.getElementById('progressSummary').innerHTML = summaryHtml;
    }

    async generateStatsHtml() {
        let html = '';
        
        for (const [examKey, examData] of Object.entries(this.syllabi)) {
            try {
                const response = await fetch(`/api/stats/${examKey}`);
                const stats = await response.json();
                
                html += `
                    <div class="stat-card">
                        <h3>${examData.name}</h3>
                        <div class="stat-number">${stats.completion_percentage}%</div>
                        <p>${stats.completed_topics}/${stats.total_topics} topics completed</p>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${stats.completion_percentage}%"></div>
                        </div>
                    </div>
                `;
            } catch (error) {
                console.error(`Error loading stats for ${examKey}:`, error);
            }
        }
        
        return html;
    }

    async generateProgressSummaryHtml() {
        let html = `
            <h3 class="summary-title">Overall Progress Summary</h3>
            <div class="summary-grid">
        `;
        
        for (const [examKey, examData] of Object.entries(this.syllabi)) {
            try {
                const response = await fetch(`/api/stats/${examKey}`);
                const stats = await response.json();
                
                html += `
                    <div class="summary-item">
                        <h4>${examData.name}</h4>
                        <div class="summary-percentage">${stats.completion_percentage}%</div>
                        <p>${stats.completed_topics}/${stats.total_topics}</p>
                    </div>
                `;
            } catch (error) {
                console.error(`Error loading summary for ${examKey}:`, error);
            }
        }
        
        html += '</div>';
        return html;
    }

    formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-IN', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        });
    }

    showLoading() {
        document.getElementById('loading').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast ${type} show`;
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ExamTracker();
});
