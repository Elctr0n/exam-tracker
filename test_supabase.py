#!/usr/bin/env python3
"""
Test script to verify Supabase connection
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test the database connection
try:
    from database import db
    print("✅ Database module imported successfully")
    print(f"📊 Database type: {db.db_type}")
    
    if db.db_type == 'postgresql':
        print("🎉 Successfully connected to Supabase PostgreSQL!")
        print("🔗 Connection details:")
        print(f"   - Host: {db.connection.info.host}")
        print(f"   - Port: {db.connection.info.port}")
        print(f"   - Database: {db.connection.info.dbname}")
        print(f"   - User: {db.connection.info.user}")
    else:
        print("⚠️  Using SQLite (local development mode)")
        print("💡 Make sure to create .env file with DATABASE_URL")
        
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("💡 Make sure:")
    print("   1. You created a .env file")
    print("   2. DATABASE_URL is set correctly")
    print("   3. Your Supabase password is correct")
