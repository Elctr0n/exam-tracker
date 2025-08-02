#!/usr/bin/env python3
"""
Test Supabase database connectivity
"""

import os
import sys
from urllib.parse import urlparse

def test_supabase_connection():
    """Test direct connection to Supabase"""
    print("🔍 Testing Supabase Database Connection")
    print("=" * 50)
    
    # Test connection string
    supabase_url = "postgresql://postgres:8a4osq4qVwS5ZQAA@db.tkdcbjtrgeufbbhfmklo.supabase.co:5432/postgres"
    
    # Parse URL
    url = urlparse(supabase_url)
    print(f"🏠 Host: {url.hostname}")
    print(f"🔌 Port: {url.port}")
    print(f"👤 User: {url.username}")
    print(f"🗄️ Database: {url.path[1:] if url.path else 'postgres'}")
    
    # Test with both psycopg versions
    print("\n🧪 Testing psycopg3...")
    try:
        import psycopg as psycopg2
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port or 5432,
            user=url.username,
            password=url.password,
            dbname=url.path[1:] if url.path else 'postgres',
            sslmode='require',
            connect_timeout=10  # 10 second timeout
        )
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ psycopg3 connection successful!")
        print(f"📊 PostgreSQL version: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("❌ psycopg3 not available")
    except Exception as e:
        print(f"❌ psycopg3 connection failed: {e}")
    
    print("\n🧪 Testing psycopg2...")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port or 5432,
            user=url.username,
            password=url.password,
            database=url.path[1:] if url.path else 'postgres',
            sslmode='require',
            connect_timeout=10  # 10 second timeout
        )
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ psycopg2 connection successful!")
        print(f"📊 PostgreSQL version: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("❌ psycopg2 not available")
    except Exception as e:
        print(f"❌ psycopg2 connection failed: {e}")
    
    return False

def test_network_connectivity():
    """Test basic network connectivity"""
    print("\n🌐 Testing Network Connectivity")
    print("=" * 50)
    
    import socket
    
    try:
        # Test DNS resolution
        host = "db.tkdcbjtrgeufbbhfmklo.supabase.co"
        ip = socket.gethostbyname(host)
        print(f"✅ DNS resolution successful: {host} -> {ip}")
        
        # Test port connectivity
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((ip, 5432))
        sock.close()
        
        if result == 0:
            print("✅ Port 5432 is reachable")
            return True
        else:
            print(f"❌ Port 5432 is not reachable (error code: {result})")
            return False
            
    except Exception as e:
        print(f"❌ Network test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔬 Supabase Database Connectivity Test")
    print("=" * 60)
    
    # Test network first
    network_ok = test_network_connectivity()
    
    # Test database connection
    db_ok = test_supabase_connection()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"🌐 Network Connectivity: {'✅ OK' if network_ok else '❌ FAILED'}")
    print(f"🗄️ Database Connection: {'✅ OK' if db_ok else '❌ FAILED'}")
    
    if network_ok and db_ok:
        print("🎉 All tests passed! Supabase is accessible.")
        return 0
    else:
        print("❌ Some tests failed. Check Supabase status and network connectivity.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
