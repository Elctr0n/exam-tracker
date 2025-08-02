# ExamX - Advanced Exam Tracker

🎯 **A comprehensive exam preparation tracker built for students, by students.**

ExamX is a modern, feature-rich web application designed to help students track their exam preparation progress across multiple subjects and topics. Built with Flask, PostgreSQL, and a beautiful cyber-neon UI.

## ✨ Features

### 📚 **Core Functionality**
- **Multi-Exam Support**: Track progress for JEE, NEET, GATE, CAT, and more
- **Three-Stage Learning**: Theory → Practice → Revision workflow
- **Real-time Progress Tracking**: Visual progress indicators and statistics
- **Persistent Study Timer**: Cross-tab synchronized timer with play/pause/stop controls

### 🎨 **User Experience**
- **Cyber-Neon Theme**: Modern, professional dark theme with neon accents
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Feather Icons**: Consistent, professional iconography throughout
- **Smooth Animations**: Enhanced user interactions and transitions

### 🔧 **Advanced Features**
- **Firebase Authentication**: Secure user login and session management
- **Supabase Integration**: Robust PostgreSQL database with real-time sync
- **Account Settings**: Study reminders, dark mode, privacy controls
- **Activity Tracking**: Comprehensive analytics and progress insights
- **Cross-Device Sync**: Settings and progress synchronized across devices

### 📊 **Analytics & Insights**
- **Detailed Statistics**: Study time, completion rates, streak tracking
- **Progress Visualization**: Charts and graphs for performance analysis
- **Study Session Management**: Track focused study periods
- **Achievement System**: Milestones and progress celebrations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for local development)
- Firebase project (for authentication)
- Supabase account (for production database)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Elctr0n/exam-tracker.git
   cd exam-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file with your configuration
   DATABASE_URL=your_database_url_here
   FLASK_ENV=development
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the app**
   Open `http://localhost:5000` in your browser

## 🌐 Deployment

### Deploy to Render

ExamX is configured for easy deployment to Render:

1. **Fork this repository** to your GitHub account

2. **Create a new Web Service** on [Render](https://render.com)

3. **Connect your GitHub repository**

4. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

5. **Set environment variables**:
   - `DATABASE_URL`: Your Supabase PostgreSQL connection string
   - `FLASK_ENV`: `production`
   - `RENDER_ENVIRONMENT`: `production`

6. **Deploy** and access your live app!

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/syllabi` - Get all exam syllabi
- `GET /api/progress/<exam>` - Get progress for specific exam
- `POST /api/progress/<exam>` - Update progress for specific exam
- `POST /api/toggle-topic` - Toggle topic completion status
- `GET /api/stats/<exam>` - Get completion statistics for exam

## Features in Detail

### Progress Tracking
- Individual topic completion with timestamps
- Subject-wise progress calculation
- Overall exam completion percentages
- Visual progress bars and statistics

### User Interface
- Responsive design for all devices
- Modern gradient backgrounds
- Smooth animations and transitions
- Intuitive tab-based navigation
- Toast notifications for user feedback

### Data Management
- Automatic progress saving
- JSON-based data storage
- Easy migration to database systems
- Session-based user identification

## Customization

The application is designed to be easily customizable:

1. **Add New Exams**: Extend the `get_exam_syllabi()` function in `app.py`
2. **Modify Syllabi**: Update topic lists in the syllabi data structure
3. **UI Customization**: Modify CSS variables and styles in `style.css`
4. **Database Integration**: Replace JSON storage with database queries

## Browser Compatibility

- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+

## Contributing

Feel free to contribute by:
- Adding more exam syllabi
- Improving the UI/UX
- Adding new features like study schedules
- Implementing user authentication
- Adding data export functionality

## License

This project is open source and available under the MIT License.
