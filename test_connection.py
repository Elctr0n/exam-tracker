#!/usr/bin/env python3
"""
Test different Supabase connection methods
"""
import psycopg2
from urllib.parse import urlparse

def test_connection(connection_string, description):
    """Test a specific connection string"""
    print(f"\n🧪 Testing {description}...")
    print(f"🔗 Connection: {connection_string[:50]}...")
    
    try:
        url = urlparse(connection_string)
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port or 5432,
            user=url.username,
            password=url.password,
            database=url.path[1:] if url.path else 'postgres',
            sslmode='require',
            connect_timeout=10  # 10 second timeout
        )
        print(f"✅ SUCCESS! Connected to {description}")
        print(f"   - Host: {url.hostname}")
        print(f"   - Port: {url.port or 5432}")
        print(f"   - Database: {url.path[1:] if url.path else 'postgres'}")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def main():
    print("🚀 Supabase Connection Troubleshooting")
    print("=" * 50)
    
    # Replace with your actual password
    password = "8a4osq4qVwS5ZQAA"  # From your setup attempt
    
    # Test different connection strings
    connections = [
        (f"postgresql://postgres:{password}@db.tkdcbjtrgeufohmfmklo.supabase.co:5432/postgres", 
         "Direct Connection"),
        (f"postgresql://postgres.tkdcbjtrgeufohmfmklo:{password}@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres", 
         "Transaction Pooler"),
        (f"postgresql://postgres.tkdcbjtrgeufohmfmklo:{password}@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres", 
         "Session Pooler")
    ]
    
    successful_connections = []
    
    for conn_str, desc in connections:
        if test_connection(conn_str, desc):
            successful_connections.append((conn_str, desc))
    
    print(f"\n📊 Results:")
    print(f"   - Successful connections: {len(successful_connections)}")
    print(f"   - Failed connections: {len(connections) - len(successful_connections)}")
    
    if successful_connections:
        print(f"\n🎉 Recommended connection string:")
        best_conn, best_desc = successful_connections[0]
        print(f"   {best_desc}: {best_conn}")
        
        # Create .env file with working connection
        with open('.env', 'w') as f:
            f.write(f"DATABASE_URL={best_conn}\n")
        print(f"\n✅ Updated .env file with working connection!")
    else:
        print(f"\n⚠️  No connections successful. Possible issues:")
        print(f"   1. Network/firewall blocking Supabase")
        print(f"   2. Incorrect password")
        print(f"   3. DNS resolution issues")
        print(f"   4. Supabase project not fully initialized")

if __name__ == "__main__":
    main()
