from database import get_db_connection

conn = get_db_connection()

if conn:
    print("✅ Successfully connected to Supabase PostgreSQL")
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("📦 PostgreSQL version:", version)
    cursor.close()
    conn.close()
else:
    print("❌ Could not establish connection")
