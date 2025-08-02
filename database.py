import psycopg2
import json
import os
from datetime import datetime
from urllib.parse import urlparse

class DatabaseManager:
    def __init__(self):
        self.db_type = None
        self.connection = None
        self.init_database()
    
    def init_database(self):
        """Initialize database connection - PostgreSQL for production, SQLite for development"""
        # Check for PostgreSQL connection (Railway provides DATABASE_URL)
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url:
            try:
                # Parse the DATABASE_URL for PostgreSQL
                url = urlparse(database_url)
                self.db_type = 'postgresql'
                
                # Handle Railway's PostgreSQL connection
                self.connection = psycopg2.connect(
                    host=url.hostname,
                    port=url.port or 5432,
                    user=url.username,
                    password=url.password,
                    database=url.path[1:] if url.path else 'railway',  # Remove leading slash
                    sslmode='require'  # Railway requires SSL
                )
                print("✅ Connected to PostgreSQL database")
                
            except Exception as e:
                print(f"❌ PostgreSQL connection failed: {e}")
                # In production (Railway), don't fall back to SQLite - raise the error
                if os.environ.get('RAILWAY_ENVIRONMENT'):
                    print("🚨 Running in Railway - SQLite fallback disabled")
                    raise Exception(f"PostgreSQL connection required in production: {e}")
                else:
                    print("🔄 Falling back to SQLite for local development...")
                    self.init_sqlite()
        else:
            # Only use SQLite for local development
            if os.environ.get('RAILWAY_ENVIRONMENT'):
                raise Exception("DATABASE_URL not found in Railway environment")
            else:
                print("🔧 Using SQLite for local development")
                self.init_sqlite()
        
        # Create tables
        self.create_tables()
    
    def init_sqlite(self):
        """Initialize SQLite database"""
        try:
            import sqlite3
        except ImportError:
            raise Exception("SQLite not available in this environment")
            
        self.db_type = 'sqlite'
        self.db_path = 'prepdyno.db'
        # Test connection
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.close()
        print("✅ Connected to SQLite database")
    
    def get_connection(self):
        """Get a database connection"""
        if self.db_type == 'postgresql':
            return self.connection
        else:
            # Create new connection for SQLite to avoid transaction issues
            import sqlite3
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            return conn
    
    def create_tables(self):
        """Create necessary tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.db_type == 'postgresql':
            # PostgreSQL syntax
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255),
                    display_name VARCHAR(255),
                    photo_url TEXT,
                    selected_exams TEXT,  -- JSON array
                    selected_exam VARCHAR(100),  -- Primary exam for backward compatibility
                    exam_selected_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_progress (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    exam VARCHAR(100) NOT NULL,
                    subject VARCHAR(100) NOT NULL,
                    topic VARCHAR(255) NOT NULL,
                    theory BOOLEAN DEFAULT FALSE,
                    practice BOOLEAN DEFAULT FALSE,
                    revision BOOLEAN DEFAULT FALSE,
                    completed_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, exam, subject, topic)
                )
            ''')
        else:
            # SQLite syntax
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    email TEXT,
                    display_name TEXT,
                    photo_url TEXT,
                    selected_exams TEXT,  -- JSON array
                    selected_exam TEXT,   -- Primary exam for backward compatibility
                    exam_selected_at TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    exam TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    theory INTEGER DEFAULT 0,
                    practice INTEGER DEFAULT 0,
                    revision INTEGER DEFAULT 0,
                    completed_at TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, exam, subject, topic)
                )
            ''')
        
        conn.commit()
        if self.db_type == 'sqlite':
            conn.close()
        print("✅ Database tables created successfully")
    
    def save_user_data(self, user_id, user_data):
        """Save or update user data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        selected_exams_json = json.dumps(user_data.get('selected_exams', []))
        selected_exam = user_data.get('selected_exam', '')
        exam_selected_at = user_data.get('exam_selected_at', datetime.now().isoformat())
        
        if self.db_type == 'postgresql':
            cursor.execute('''
                INSERT INTO users (user_id, selected_exams, selected_exam, exam_selected_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id) 
                DO UPDATE SET 
                    selected_exams = EXCLUDED.selected_exams,
                    selected_exam = EXCLUDED.selected_exam,
                    exam_selected_at = EXCLUDED.exam_selected_at,
                    updated_at = EXCLUDED.updated_at
            ''', (user_id, selected_exams_json, selected_exam, exam_selected_at, datetime.now().isoformat()))
        else:
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (user_id, selected_exams, selected_exam, exam_selected_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, selected_exams_json, selected_exam, exam_selected_at, datetime.now().isoformat()))
        
        conn.commit()
        if self.db_type == 'sqlite':
            conn.close()
    
    def get_user_data(self, user_id):
        """Get user data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.db_type == 'postgresql':
            cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        else:
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        
        row = cursor.fetchone()
        if row:
            if self.db_type == 'postgresql':
                return {
                    'user_id': row[1],
                    'selected_exams': json.loads(row[5] or '[]'),
                    'selected_exam': row[6],
                    'exam_selected_at': row[7]
                }
            else:
                return {
                    'user_id': row['user_id'],
                    'selected_exams': json.loads(row['selected_exams'] or '[]'),
                    'selected_exam': row['selected_exam'],
                    'exam_selected_at': row['exam_selected_at']
                }
        
        if self.db_type == 'sqlite':
            conn.close()
        return None
    
    def save_user_progress(self, user_id, exam, subject, topic, progress_data):
        """Save user progress for a specific topic"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        theory = progress_data.get('theory', False)
        practice = progress_data.get('practice', False)
        revision = progress_data.get('revision', False)
        completed_at = progress_data.get('completed_at')
        
        if self.db_type == 'postgresql':
            cursor.execute('''
                INSERT INTO user_progress 
                (user_id, exam, subject, topic, theory, practice, revision, completed_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id, exam, subject, topic)
                DO UPDATE SET
                    theory = EXCLUDED.theory,
                    practice = EXCLUDED.practice,
                    revision = EXCLUDED.revision,
                    completed_at = EXCLUDED.completed_at,
                    updated_at = EXCLUDED.updated_at
            ''', (user_id, exam, subject, topic, theory, practice, revision, completed_at, datetime.now().isoformat()))
        else:
            cursor.execute('''
                INSERT OR REPLACE INTO user_progress
                (user_id, exam, subject, topic, theory, practice, revision, completed_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, exam, subject, topic, int(theory), int(practice), int(revision), completed_at, datetime.now().isoformat()))
        
        conn.commit()
        if self.db_type == 'sqlite':
            conn.close()
    
    def get_user_progress(self, user_id, exam=None):
        """Get user progress data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if exam:
            if self.db_type == 'postgresql':
                cursor.execute('SELECT * FROM user_progress WHERE user_id = %s AND exam = %s', (user_id, exam))
            else:
                cursor.execute('SELECT * FROM user_progress WHERE user_id = ? AND exam = ?', (user_id, exam))
        else:
            if self.db_type == 'postgresql':
                cursor.execute('SELECT * FROM user_progress WHERE user_id = %s', (user_id,))
            else:
                cursor.execute('SELECT * FROM user_progress WHERE user_id = ?', (user_id,))
        
        rows = cursor.fetchall()
        progress = {}
        
        for row in rows:
            if self.db_type == 'postgresql':
                exam_name = row[2]
                subject = row[3]
                topic = row[4]
                theory = row[5]
                practice = row[6]
                revision = row[7]
                completed_at = row[8]
            else:
                exam_name = row['exam']
                subject = row['subject']
                topic = row['topic']
                theory = bool(row['theory'])
                practice = bool(row['practice'])
                revision = bool(row['revision'])
                completed_at = row['completed_at']
            
            if exam_name not in progress:
                progress[exam_name] = {}
            if subject not in progress[exam_name]:
                progress[exam_name][subject] = {}
            
            progress[exam_name][subject][topic] = {
                'theory': theory,
                'practice': practice,
                'revision': revision,
                'completed_at': completed_at
            }
        
        if self.db_type == 'sqlite':
            conn.close()
        return progress
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

# Global database instance
db = DatabaseManager()
