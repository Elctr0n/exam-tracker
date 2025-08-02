# Exam Syllabus Completion & Preparation Tracker

A comprehensive web application to track syllabus completion and preparation progress for major engineering entrance exams including JEE Main, JEE Advanced, IAT (Indian Army Technical), and UGEE (Undergraduate Engineering Entrance Exam).

## Features

- **Multi-Exam Support**: Track progress for JEE Main, JEE Advanced, IAT, and UGEE
- **Subject-wise Organization**: Organized by subjects (Physics, Chemistry, Mathematics, General Knowledge)
- **Topic-level Tracking**: Mark individual topics as completed with timestamps
- **Progress Visualization**: Real-time progress bars and completion percentages
- **Modern UI**: Clean, responsive, and user-friendly interface
- **Data Persistence**: Progress is saved automatically and persists between sessions
- **Statistics Dashboard**: Overview of completion status across all exams

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Modern CSS with gradients and animations
- **Icons**: Font Awesome
- **Data Storage**: JSON file (easily upgradeable to database)

## Installation & Setup

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your web browser and navigate to `http://localhost:5000`

## Usage

1. **Select an Exam**: Click on the exam tabs (JEE Main, JEE Advanced, IAT, UGEE)
2. **Track Progress**: Click on topic checkboxes to mark them as completed
3. **View Statistics**: Monitor your progress through the stats cards and progress bars
4. **Subject-wise Progress**: Each subject shows individual completion percentages

## Exam Syllabi Included

### JEE Main
- **Physics**: 14 major topics including Mechanics, Thermodynamics, Electromagnetism, Optics, Modern Physics
- **Chemistry**: 20 topics covering Physical, Inorganic, and Organic Chemistry
- **Mathematics**: 15 topics including Calculus, Algebra, Coordinate Geometry, Statistics

### JEE Advanced
- **Physics**: 6 comprehensive areas
- **Chemistry**: 3 major branches
- **Mathematics**: 6 core areas

### IAT (Indian Army Technical)
- **Mathematics**: 6 fundamental topics
- **Physics**: 6 core areas
- **Chemistry**: 3 main branches
- **General Knowledge**: 6 important areas

### UGEE
- **Physics**: 10 comprehensive topics
- **Chemistry**: 25 detailed topics
- **Mathematics**: 16 core areas

## File Structure

```
exam-tracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── user_progress.json    # User progress data (auto-generated)
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Styling and responsive design
    └── js/
        └── app.js        # Frontend JavaScript logic
```

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
