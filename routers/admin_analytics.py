from fastapi import APIRouter
from database import get_db_connection

router = APIRouter(
    prefix="/admin/analytics",
    tags=["Admin Analytics"]
)

@router.get("/clinics")
def clinics_with_most_services():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.clinic_name,
            COUNT(a.id) AS total_services
        FROM appointments a
        JOIN clinic c ON a.id_clinic = c.id_clinic
        GROUP BY c.clinic_name
        ORDER BY total_services DESC
        LIMIT 5
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "labels": [r[0] for r in rows],
        "datasets": [
            {
                "label": "Services per clinic",
                "data": [r[1] for r in rows]
            }
        ]
    }


@router.get("/animals")
def most_attended_animals():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            an.animal_name,
            COUNT(a.id) AS total_services
        FROM appointments a
        JOIN pets p ON a.id_pet = p.id_pet
        JOIN animals an ON p.id_animal = an.id_animal
        GROUP BY an.animal_name
        ORDER BY total_services DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "labels": [r[0] for r in rows],
        "datasets": [
            {
                "label": "Services by animal type",
                "data": [r[1] for r in rows]
            }
        ]
    }


@router.get("/clients-by-month")
def clients_by_month():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            TO_CHAR(a."createdAt", 'YYYY-MM') AS month,
            COUNT(DISTINCT a.id_user) AS total_clients
        FROM appointments a
        GROUP BY month
        ORDER BY month
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "labels": [r[0] for r in rows],
        "datasets": [
            {
                "label": "Clients per month",
                "data": [r[1] for r in rows]
            }
        ]
    }


@router.get("/top-clients")
def top_clients(limit: int = 5):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            u.full_name,
            COUNT(a.id) AS total_services
        FROM appointments a
        JOIN users u ON a.id_user = u.id_user
        GROUP BY u.full_name
        ORDER BY total_services DESC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "client": r[0],
            "total_services": r[1]
        }
        for r in rows
    ]


@router.get("/services")
def services_most_requested():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            t.name AS service,
            COUNT(a.id) AS total_services
        FROM appointments a
        JOIN appointments_types t ON a.id_type = t.id
        GROUP BY t.name
        ORDER BY total_services DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "service": r[0],
            "total_services": r[1]
        }
        for r in rows
    ]


@router.get("/services-by-period")
def services_by_period(period: str = "month"):
    conn = get_db_connection()
    cur = conn.cursor()

    if period == "day":
        group = "YYYY-MM-DD"
    elif period == "year":
        group = "YYYY"
    else:
        group = "YYYY-MM"

    cur.execute(f"""
        SELECT
            TO_CHAR(a."createdAt", '{group}') AS period,
            COUNT(a.id) AS total_services
        FROM appointments a
        WHERE a."createdAt" IS NOT NULL
        GROUP BY period
        ORDER BY period
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "period": r[0],
            "total_services": r[1]
        }
        for r in rows
    ]


@router.get("/kpis/summary")
def kpis_summary():
    """
    Returns general KPIs for the Admin dashboard:
    - Total revenue
    - Average revenue per appointment
    - Total number of appointments
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Total revenue
    cur.execute("SELECT SUM(amount) FROM appointments")
    total_revenue = cur.fetchone()[0] or 0

    # Average revenue per appointment
    cur.execute("SELECT AVG(amount) FROM appointments")
    avg_revenue = cur.fetchone()[0] or 0

    # Total appointments
    cur.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "total_revenue": float(total_revenue),
        "avg_revenue": float(avg_revenue),
        "total_appointments": total_appointments
    }
