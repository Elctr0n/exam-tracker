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
        # Check for PostgreSQL connection (Supabase provides DATABASE_URL)
        database_url = (
            os.environ.get('DATABASE_URL') or 
            os.environ.get('SUPABASE_DB_URL') or
            os.environ.get('POSTGRES_URL')
        )
        
        if database_url:
            try:
                # Parse the DATABASE_URL for PostgreSQL
                url = urlparse(database_url)
                self.db_type = 'postgresql'
                
                # Connect to Supabase PostgreSQL
                self.connection = psycopg2.connect(
                    host=url.hostname,
                    port=url.port or 5432,
                    user=url.username,
                    password=url.password,
                    database=url.path[1:] if url.path else 'postgres',  # Remove leading slash
                    sslmode='require'  # Supabase requires SSL
                )
                print("✅ Connected to Supabase PostgreSQL database")
                
            except Exception as e:
                print(f"❌ PostgreSQL connection failed: {e}")
                # Check if we're in production environment
                is_production = any([
                    os.environ.get('RAILWAY_ENVIRONMENT'),
                    os.environ.get('VERCEL'),
                    os.environ.get('NETLIFY'),
                    os.environ.get('HEROKU'),
                    os.environ.get('PORT')  # Most platforms set PORT
                ])
                if is_production:
                    print("🚨 Running in production - PostgreSQL connection required")
                    raise Exception(f"PostgreSQL connection required in production: {e}")
                else:
                    print("🔄 Falling back to SQLite for local development...")
                    self.init_sqlite()
        else:
            # Check if we're in production environment
            is_production = any([
                os.environ.get('RAILWAY_ENVIRONMENT'),
                os.environ.get('VERCEL'),
                os.environ.get('NETLIFY'),
                os.environ.get('HEROKU'),
                os.environ.get('PORT')  # Most platforms set PORT
            ])
            if is_production:
                print(f"🚨 Production environment detected but DATABASE_URL not found!")
                print(f"Available env vars: {[k for k in os.environ.keys() if 'DATABASE' in k or 'POSTGRES' in k or 'SUPABASE' in k]}")
                raise Exception("DATABASE_URL not found in production environment")
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
            
            # User settings and preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) UNIQUE NOT NULL,
                    study_reminders BOOLEAN DEFAULT TRUE,
                    dark_mode BOOLEAN DEFAULT FALSE,
                    privacy_mode BOOLEAN DEFAULT FALSE,
                    notification_preferences JSONB DEFAULT '{}',
                    theme_preferences JSONB DEFAULT '{}',
                    study_schedule JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User activity and analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_activity (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    activity_type VARCHAR(100) NOT NULL,
                    activity_data JSONB DEFAULT '{}',
                    exam VARCHAR(100),
                    subject VARCHAR(100),
                    topic VARCHAR(255),
                    session_duration INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Study sessions tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS study_sessions (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    exam VARCHAR(100) NOT NULL,
                    subject VARCHAR(100),
                    topic VARCHAR(255),
                    session_start TIMESTAMP NOT NULL,
                    session_end TIMESTAMP,
                    duration_minutes INTEGER DEFAULT 0,
                    session_type VARCHAR(50) DEFAULT 'study',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User statistics and achievements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_statistics (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) UNIQUE NOT NULL,
                    total_study_time INTEGER DEFAULT 0,
                    study_streak INTEGER DEFAULT 0,
                    last_study_date DATE,
                    total_topics_completed INTEGER DEFAULT 0,
                    total_exams_started INTEGER DEFAULT 0,
                    achievements JSONB DEFAULT '[]',
                    weekly_goals JSONB DEFAULT '{}',
                    monthly_stats JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            
            # User settings and preferences table (SQLite)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    study_reminders INTEGER DEFAULT 1,
                    dark_mode INTEGER DEFAULT 0,
                    privacy_mode INTEGER DEFAULT 0,
                    notification_preferences TEXT DEFAULT '{}',
                    theme_preferences TEXT DEFAULT '{}',
                    study_schedule TEXT DEFAULT '{}',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User activity and analytics table (SQLite)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    activity_data TEXT DEFAULT '{}',
                    exam TEXT,
                    subject TEXT,
                    topic TEXT,
                    session_duration INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Study sessions tracking table (SQLite)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS study_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    exam TEXT NOT NULL,
                    subject TEXT,
                    topic TEXT,
                    session_start TEXT NOT NULL,
                    session_end TEXT,
                    duration_minutes INTEGER DEFAULT 0,
                    session_type TEXT DEFAULT 'study',
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User statistics and achievements table (SQLite)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    total_study_time INTEGER DEFAULT 0,
                    study_streak INTEGER DEFAULT 0,
                    last_study_date TEXT,
                    total_topics_completed INTEGER DEFAULT 0,
                    total_exams_started INTEGER DEFAULT 0,
                    achievements TEXT DEFAULT '[]',
                    weekly_goals TEXT DEFAULT '{}',
                    monthly_stats TEXT DEFAULT '{}',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')         
        conn.commit()
        if self.db_type == 'sqlite':
            conn.close()
        print("✅ Database tables created successfully")
    print("📊 Enhanced schema: users, user_progress, user_settings, user_activity, study_sessions, user_statistics")

    # User Settings Methods
    def save_user_settings(self, user_id, settings):
        """Save user settings and preferences"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db_type == 'postgresql':
                cursor.execute('''
                    INSERT INTO user_settings (user_id, study_reminders, dark_mode, privacy_mode, 
                                              notification_preferences, theme_preferences, study_schedule, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (user_id) DO UPDATE SET
                        study_reminders = EXCLUDED.study_reminders,
                        dark_mode = EXCLUDED.dark_mode,
                        privacy_mode = EXCLUDED.privacy_mode,
                        notification_preferences = EXCLUDED.notification_preferences,
                        theme_preferences = EXCLUDED.theme_preferences,
                        study_schedule = EXCLUDED.study_schedule,
                        updated_at = CURRENT_TIMESTAMP
                ''', (
                    user_id,
                    settings.get('study_reminders', True),
                    settings.get('dark_mode', False),
                    settings.get('privacy_mode', False),
                    json.dumps(settings.get('notification_preferences', {})),
                    json.dumps(settings.get('theme_preferences', {})),
                    json.dumps(settings.get('study_schedule', {}))
                ))
            else:
                cursor.execute('''
                    INSERT OR REPLACE INTO user_settings (user_id, study_reminders, dark_mode, privacy_mode,
                                                         notification_preferences, theme_preferences, study_schedule)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    1 if settings.get('study_reminders', True) else 0,
                    1 if settings.get('dark_mode', False) else 0,
                    1 if settings.get('privacy_mode', False) else 0,
                    json.dumps(settings.get('notification_preferences', {})),
                    json.dumps(settings.get('theme_preferences', {})),
                    json.dumps(settings.get('study_schedule', {}))
                ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving user settings: {e}")
            return False
        finally:
            if self.db_type == 'sqlite':
                conn.close()
    
    def get_user_settings(self, user_id):
        """Get user settings and preferences"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM user_settings WHERE user_id = %s' if self.db_type == 'postgresql' else 'SELECT * FROM user_settings WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in cursor.description]
                settings = dict(zip(columns, result))
                
                # Parse JSON fields
                for field in ['notification_preferences', 'theme_preferences', 'study_schedule']:
                    if field in settings and settings[field]:
                        try:
                            settings[field] = json.loads(settings[field])
                        except:
                            settings[field] = {}
                
                # Convert boolean fields for SQLite
                if self.db_type == 'sqlite':
                    settings['study_reminders'] = bool(settings['study_reminders'])
                    settings['dark_mode'] = bool(settings['dark_mode'])
                    settings['privacy_mode'] = bool(settings['privacy_mode'])
                
                return settings
            return None
        except Exception as e:
            print(f"Error getting user settings: {e}")
            return None
        finally:
            if self.db_type == 'sqlite':
                conn.close()
    
    def log_user_activity(self, user_id, activity_type, activity_data=None, exam=None, subject=None, topic=None, session_duration=0):
        """Log user activity for analytics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db_type == 'postgresql':
                cursor.execute('''
                    INSERT INTO user_activity (user_id, activity_type, activity_data, exam, subject, topic, session_duration)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
                    user_id,
                    activity_type,
                    json.dumps(activity_data or {}),
                    exam,
                    subject,
                    topic,
                    session_duration
                ))
            else:
                cursor.execute('''
                    INSERT INTO user_activity (user_id, activity_type, activity_data, exam, subject, topic, session_duration)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    activity_type,
                    json.dumps(activity_data or {}),
                    exam,
                    subject,
                    topic,
                    session_duration
                ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging user activity: {e}")
            return False
        finally:
            if self.db_type == 'sqlite':
                conn.close()
    
    def start_study_session(self, user_id, exam, subject=None, topic=None, session_type='study'):
        """Start a new study session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db_type == 'postgresql':
                cursor.execute('''
                    INSERT INTO study_sessions (user_id, exam, subject, topic, session_start, session_type)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
                    RETURNING id
                ''', (user_id, exam, subject, topic, session_type))
                session_id = cursor.fetchone()[0]
            else:
                cursor.execute('''
                    INSERT INTO study_sessions (user_id, exam, subject, topic, session_start, session_type)
                    VALUES (?, ?, ?, ?, datetime('now'), ?)
                ''', (user_id, exam, subject, topic, session_type))
                session_id = cursor.lastrowid
            
            conn.commit()
            return session_id
        except Exception as e:
            print(f"Error starting study session: {e}")
            return None
        finally:
            if self.db_type == 'sqlite':
                conn.close()
    
    def end_study_session(self, session_id, notes=None):
        """End a study session and calculate duration"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db_type == 'postgresql':
                cursor.execute('''
                    UPDATE study_sessions 
                    SET session_end = CURRENT_TIMESTAMP,
                        duration_minutes = EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - session_start))/60,
                        notes = %s
                    WHERE id = %s
                    RETURNING user_id, duration_minutes
                ''', (notes, session_id))
                result = cursor.fetchone()
            else:
                cursor.execute('''
                    UPDATE study_sessions 
                    SET session_end = datetime('now'),
                        duration_minutes = (julianday(datetime('now')) - julianday(session_start)) * 24 * 60,
                        notes = ?
                    WHERE id = ?
                ''', (notes, session_id))
                
                cursor.execute('SELECT user_id, duration_minutes FROM study_sessions WHERE id = ?', (session_id,))
                result = cursor.fetchone()
            
            conn.commit()
            
            if result:
                user_id, duration = result
                # Update user statistics
                self.update_user_statistics(user_id, study_time_added=int(duration or 0))
                return duration
            return None
        except Exception as e:
            print(f"Error ending study session: {e}")
            return None
        finally:
            if self.db_type == 'sqlite':
                conn.close()
    
    def update_user_statistics(self, user_id, study_time_added=0, topics_completed=0):
        """Update user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get current statistics
            cursor.execute('SELECT * FROM user_statistics WHERE user_id = %s' if self.db_type == 'postgresql' else 'SELECT * FROM user_statistics WHERE user_id = ?', (user_id,))
            current_stats = cursor.fetchone()
            
            if current_stats:
                # Update existing statistics
                new_total_time = (current_stats[2] or 0) + study_time_added
                new_topics_completed = (current_stats[5] or 0) + topics_completed
                
                if self.db_type == 'postgresql':
                    cursor.execute('''
                        UPDATE user_statistics 
                        SET total_study_time = %s,
                            total_topics_completed = %s,
                            last_study_date = CURRENT_DATE,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = %s
                    ''', (new_total_time, new_topics_completed, user_id))
                else:
                    cursor.execute('''
                        UPDATE user_statistics 
                        SET total_study_time = ?,
                            total_topics_completed = ?,
                            last_study_date = date('now')
                        WHERE user_id = ?
                    ''', (new_total_time, new_topics_completed, user_id))
            else:
                # Create new statistics record
                if self.db_type == 'postgresql':
                    cursor.execute('''
                        INSERT INTO user_statistics (user_id, total_study_time, total_topics_completed, last_study_date)
                        VALUES (%s, %s, %s, CURRENT_DATE)
                    ''', (user_id, study_time_added, topics_completed))
                else:
                    cursor.execute('''
                        INSERT INTO user_statistics (user_id, total_study_time, total_topics_completed, last_study_date)
                        VALUES (?, ?, ?, date('now'))
                    ''', (user_id, study_time_added, topics_completed))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user statistics: {e}")
            return False
        finally:
            if self.db_type == 'sqlite':
                conn.close()
    
    def get_user_statistics(self, user_id):
        """Get comprehensive user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get basic statistics
            cursor.execute('SELECT * FROM user_statistics WHERE user_id = %s' if self.db_type == 'postgresql' else 'SELECT * FROM user_statistics WHERE user_id = ?', (user_id,))
            stats_result = cursor.fetchone()
            
            # Get progress statistics
            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT exam) as total_exams,
                    COUNT(*) as total_topics,
                    SUM(CASE WHEN theory = %s OR practice = %s OR revision = %s THEN 1 ELSE 0 END) as completed_topics
                FROM user_progress 
                WHERE user_id = %s
            ''' if self.db_type == 'postgresql' else '''
                SELECT 
                    COUNT(DISTINCT exam) as total_exams,
                    COUNT(*) as total_topics,
                    SUM(CASE WHEN theory = 1 OR practice = 1 OR revision = 1 THEN 1 ELSE 0 END) as completed_topics
                FROM user_progress 
                WHERE user_id = ?
            ''', (True, True, True, user_id) if self.db_type == 'postgresql' else (user_id,))
            progress_result = cursor.fetchone()
            
            # Get recent activity
            cursor.execute('''
                SELECT COUNT(*) as recent_sessions
                FROM study_sessions 
                WHERE user_id = %s AND session_start >= %s
            ''' if self.db_type == 'postgresql' else '''
                SELECT COUNT(*) as recent_sessions
                FROM study_sessions 
                WHERE user_id = ? AND session_start >= date('now', '-7 days')
            ''', (user_id, 'CURRENT_DATE - INTERVAL \'7 days\'') if self.db_type == 'postgresql' else (user_id,))
            activity_result = cursor.fetchone()
            
            # Combine all statistics
            stats = {
                'total_study_time': stats_result[2] if stats_result else 0,
                'study_streak': stats_result[3] if stats_result else 0,
                'last_study_date': stats_result[4] if stats_result else None,
                'total_topics_completed': stats_result[5] if stats_result else 0,
                'total_exams_started': stats_result[6] if stats_result else 0,
                'total_exams': progress_result[0] if progress_result else 0,
                'total_topics': progress_result[1] if progress_result else 0,
                'completed_topics': progress_result[2] if progress_result else 0,
                'recent_sessions': activity_result[0] if activity_result else 0
            }
            
            return stats
        except Exception as e:
            print(f"Error getting user statistics: {e}")
            return {}
        finally:
            if self.db_type == 'sqlite':
                conn.close()

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

# Import json for database methods
import json
