from database import get_db_connection

conn = get_db_connection()

if conn:
    print("✅ Conexión exitosa a Supabase PostgreSQL")
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("📦 PostgreSQL version:", version)
    cursor.close()
    conn.close()
else:
    print("❌ No se pudo establecer conexión")
