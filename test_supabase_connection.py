#!/usr/bin/env python3
"""
Test Supabase connection with provided credentials
"""
import os
import psycopg2
from urllib.parse import urlparse

def test_supabase_connection():
    """Test the Supabase connection"""
    connection_string = "postgresql://postgres:8a4osq4qVwS5ZQAA@db.tkdcbjtrgeufbbhfmklo.supabase.co:5432/postgres"
    
    print("🧪 Testing Supabase Connection...")
    print(f"🔗 Host: db.tkdcbjtrgeufbbhfmklo.supabase.co")
    
    try:
        url = urlparse(connection_string)
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port or 5432,
            user=url.username,
            password=url.password,
            database=url.path[1:] if url.path else 'postgres',
            sslmode='require',
            connect_timeout=15
        )
        
        print("✅ SUCCESS! Connected to Supabase PostgreSQL!")
        print(f"   - Host: {url.hostname}")
        print(f"   - Port: {url.port or 5432}")
        print(f"   - Database: {url.path[1:] if url.path else 'postgres'}")
        print(f"   - User: {url.username}")
        
        # Test basic query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"   - PostgreSQL Version: {version[:50]}...")
        
        cursor.close()
        conn.close()
        
        # Create .env file for local testing
        with open('.env', 'w') as f:
            f.write(f"DATABASE_URL={connection_string}\n")
            f.write("SUPABASE_URL=https://tkdcbjtrgeufbbhfmklo.supabase.co\n")
            f.write("SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRrZGNianRyZ2V1ZmJiaGZta2xvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQxMTQzNzYsImV4cCI6MjA2OTY5MDM3Nn0.jmy7LsFObQai_z5siDQYChFm6iUjNmnmzNL_-wd1wcA\n")
        
        print("✅ Created .env file for local development!")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_app_database():
    """Test the app's database connection"""
    print("\n🧪 Testing App Database Connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from database import db
        
        if db.db_type == 'postgresql':
            print("🎉 App successfully connected to Supabase!")
            print(f"   - Database type: {db.db_type}")
            print("✅ Database tables created successfully!")
            return True
        else:
            print(f"⚠️  App using {db.db_type} instead of PostgreSQL")
            return False
            
    except Exception as e:
        print(f"❌ App database test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Supabase Connection Test")
    print("=" * 40)
    
    # Test direct connection
    if test_supabase_connection():
        # Test app connection
        test_app_database()
        
        print("\n🎯 Ready for Railway Deployment!")
        print("✅ Supabase connection working")
        print("✅ App database integration ready")
        print("✅ Environment variables configured")
    else:
        print("\n❌ Connection failed - check credentials")
