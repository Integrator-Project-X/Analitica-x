from typing import Optional
from fastapi import APIRouter, Query
from database import get_db_connection

router = APIRouter(
    prefix="/veterinarian/analytics",
    tags=["Veterinarian Analytics"]
)


@router.get("/top-clients")
def top_clients_by_clinic(
    clinic_id: int,
    limit: int = 5
):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            u.full_name,
            COUNT(a.id) AS total_visits
        FROM appointments a
        JOIN users u ON a.id_user = u.id_user
        WHERE a.id_clinic = %s
        GROUP BY u.full_name
        ORDER BY total_visits DESC
        LIMIT %s
    """, (clinic_id, limit))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {"client": r[0], "total_visits": r[1]}
        for r in rows
    ]


@router.get("/top-services")
def top_services(clinic_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            at.name,
            COUNT(a.id) AS total
        FROM appointments a
        JOIN appointments_types at ON a.id_type = at.id
        WHERE a.id_clinic = %s
        GROUP BY at.name
        ORDER BY total DESC
        LIMIT 5
    """, (clinic_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "labels": [r[0] for r in rows],
        "datasets": [
            {
                "label": "Most requested services",
                "data": [r[1] for r in rows]
            }
        ]
    }


@router.get("/services-by-period")
def services_by_period(
    clinic_id: int,
    year: int,
    month: int | None = None
):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT
            DATE(a."createdAt") AS date,
            COUNT(a.id) AS total
        FROM appointments a
        WHERE a.id_clinic = %s
          AND EXTRACT(YEAR FROM a."createdAt") = %s
    """
    params = [clinic_id, year]

    if month:
        query += " AND EXTRACT(MONTH FROM a.\"createdAt\") = %s"
        params.append(month)

    query += " GROUP BY date ORDER BY date"

    cur.execute(query, tuple(params))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "labels": [r[0].strftime("%Y-%m-%d") for r in rows],
        "datasets": [
            {
                "label": "Services performed",
                "data": [r[1] for r in rows]
            }
        ]
    }

