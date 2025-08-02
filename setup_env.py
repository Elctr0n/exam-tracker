#!/usr/bin/env python3
"""
Setup script to create .env file with Supabase credentials
"""
import os

def create_env_file():
    """Create .env file with Supabase configuration"""
    
    print("🔧 Setting up Supabase connection...")
    print("\nFrom your Supabase dashboard, I can see:")
    print("📍 Host: db.tkdcbjtrgeufohmfmklo.supabase.co")
    print("🔌 Port: 5432")
    print("👤 User: postgres")
    print("🗄️  Database: postgres")
    
    # Get password from user
    password = input("\n🔑 Enter your Supabase database password: ").strip()
    
    if not password:
        print("❌ Password cannot be empty!")
        return False
    
    # Create the connection string
    database_url = f"postgresql://postgres:{password}@db.tkdcbjtrgeufohmfmklo.supabase.co:5432/postgres"
    
    # Create .env file content
    env_content = f"""# Supabase Database Configuration
DATABASE_URL={database_url}

# Optional: Supabase API details (for future use)
SUPABASE_URL=https://tkdcbjtrgeufohmfmklo.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRrZGNianRyZ2V1Zm9obWZta2xvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMxMDEzMjQsImV4cCI6MjA0ODY3NzMyNH0.yJpc3MfOI3zxMt
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_connection():
    """Test the database connection"""
    print("\n🧪 Testing database connection...")
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Test database connection
        from database import db
        
        if db.db_type == 'postgresql':
            print("🎉 SUCCESS! Connected to Supabase PostgreSQL!")
            print(f"🔗 Connection details:")
            print(f"   - Host: {db.connection.info.host}")
            print(f"   - Port: {db.connection.info.port}")
            print(f"   - Database: {db.connection.info.dbname}")
            print(f"   - User: {db.connection.info.user}")
            print("✅ Database tables created successfully!")
            return True
        else:
            print("⚠️  Still using SQLite - check your .env file")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check your password is correct")
        print("   2. Verify your Supabase project is active")
        print("   3. Check your internet connection")
        return False

if __name__ == "__main__":
    print("🚀 Supabase Setup for Exam Tracker")
    print("=" * 40)
    
    if create_env_file():
        test_connection()
    
    print("\n🎯 Next steps:")
    print("   1. If connection successful, your app is ready!")
    print("   2. Run: python app.py")
    print("   3. Deploy to your preferred platform")
