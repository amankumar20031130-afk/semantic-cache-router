from fastapi import APIRouter

from app.database import get_connection


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)


@router.get("/summary")
def get_summary():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total_requests
        FROM requests
    """)
    total_requests = cursor.fetchone()["total_requests"]

    cursor.execute("""
        SELECT COUNT(*) AS cache_hits
        FROM requests
        WHERE cache_hit = 1
    """)
    cache_hits = cursor.fetchone()["cache_hits"]

    cursor.execute("""
        SELECT COALESCE(SUM(cost), 0) AS total_cost
        FROM requests
    """)
    total_cost = cursor.fetchone()["total_cost"]

    cursor.execute("""
        SELECT COALESCE(AVG(latency_ms), 0) AS average_latency
        FROM requests
    """)
    average_latency = cursor.fetchone()["average_latency"]

    cursor.execute("""
        SELECT COUNT(*) AS small_requests
        FROM requests
        WHERE route = 'small'
    """)
    small_requests = cursor.fetchone()["small_requests"]

    cursor.execute("""
        SELECT COUNT(*) AS large_requests
        FROM requests
        WHERE route = 'large'
    """)
    large_requests = cursor.fetchone()["large_requests"]

    connection.close()

    cache_hit_rate = (
        (cache_hits / total_requests) * 100
        if total_requests > 0
        else 0
    )

    return {
        "total_requests": total_requests,
        "cache_hits": cache_hits,
        "cache_hit_rate": round(cache_hit_rate, 2),
        "total_cost": round(total_cost, 6),
        "average_latency_ms": round(average_latency, 2),
        "small_model_requests": small_requests,
        "large_model_requests": large_requests
    }


@router.get("/requests")
def get_requests():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            query,
            cache_hit,
            similarity,
            route,
            model,
            input_tokens,
            output_tokens,
            cost,
            latency_ms,
            created_at
        FROM requests
        ORDER BY id DESC
        LIMIT 100
    """)

    rows = cursor.fetchall()

    connection.close()

    return {
        "requests": [dict(row) for row in rows]
    }