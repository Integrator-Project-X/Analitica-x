from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection

# Routers
from routers.admin_analytics import router as admin_analytics_router
from routers.veterinarian_analytics import router as veterinarian_analytics_router

app = FastAPI(
    title="Veterinary Analytics API",
    version="1.0.0"
)

# ------------------------------------
# CORS (OBLIGATORIO PARA EL FRONTEND)
# ------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
            # Admin Analytics
            "/admin/analytics/clinics",
            "/admin/analytics/animals",
            "/admin/analytics/clients-by-month",
            "/admin/analytics/kpis/summary",
            # Veterinarian Analytics
            "/veterinarian/analytics/top-clients",
            "/veterinarian/analytics/top-services",
            "/veterinarian/analytics/services-by-period",
            "/veterinarian/analytics/kpis/summary"
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
