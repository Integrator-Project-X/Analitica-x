from fastapi import FastAPI
from database import get_db_connection

# Routers
from routers.admin_analytics import router as admin_analytics_router
from routers.veterinarian_analytics import router as veterinarian_analytics_router

app = FastAPI(
    title="Veterinary Analytics API",
    version="1.0.0"
)

# ------------------------------------
# Root
# ------------------------------------
@app.get("/")
def root():
    return {
        "message": "API activa",
        "endpoints": [
            "/health/db",
            "/admin/analytics/clinics",
            "/admin/analytics/animals",
            "/admin/analytics/clients-by-month",
            "/veterinarian/analytics/top-clients",
            "/veterinarian/analytics/top-services",
            "/veterinarian/analytics/services-by-period"
        ]
    }

# ------------------------------------
# Health Check DB
# ------------------------------------
@app.get("/health/db")
def check_db():
    conn = get_db_connection()
    if not conn:
        return {
            "status": "error",
            "message": "No conecta a la base de datos"
        }

    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "status": "ok",
        "tables_in_public_schema": tables
    }

# ------------------------------------
# Routers
# ------------------------------------
app.include_router(admin_analytics_router)
app.include_router(veterinarian_analytics_router)
