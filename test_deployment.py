#!/usr/bin/env python3
"""
Test script to verify deployment readiness for ExamX app
"""

import os
import sys
import subprocess

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print("✅ Python version is compatible (3.10+ supported)")
        if version.minor >= 11:
            print("🎯 Recommended version for deployment: 3.11+")
        return True
    else:
        print("❌ Python version should be 3.10+")
        return False

def test_dependencies():
    """Test if all dependencies can be imported"""
    print("\n📦 Testing dependencies...")
    
    dependencies = [
        ('flask', 'Flask'),
        ('werkzeug', 'Werkzeug'), 
        ('gunicorn', 'Gunicorn'),
        ('psycopg2', 'psycopg2-binary')
    ]
    
    all_good = True
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name} imported successfully")
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
            all_good = False
    
    return all_good

def test_database_connection():
    """Test database connection"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from database import db
        print("✅ Database module imported successfully")
        
        # Test connection
        if db.db_type:
            print(f"✅ Database type: {db.db_type}")
            return True
        else:
            print("❌ Database connection not established")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_app_startup():
    """Test if Flask app can start"""
    print("\n🚀 Testing Flask app startup...")
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test app configuration
        if app.secret_key:
            print("✅ Secret key configured")
        else:
            print("❌ Secret key not configured")
            
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def main():
    """Run all deployment tests"""
    print("🔍 ExamX Deployment Readiness Test")
    print("=" * 40)
    
    tests = [
        test_python_version,
        test_dependencies,
        test_database_connection,
        test_app_startup
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    
    if all(results):
        print("🎉 All tests passed! App is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
