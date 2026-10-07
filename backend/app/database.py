import sqlite3


DATABASE_NAME = "metrics.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            cache_hit BOOLEAN NOT NULL,
            similarity REAL,
            route TEXT,
            model TEXT,
            input_tokens INTEGER,
            output_tokens INTEGER,
            cost REAL,
            latency_ms REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_request(
    query,
    cache_hit,
    similarity,
    route,
    model,
    input_tokens,
    output_tokens,
    cost,
    latency_ms
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO requests (
            query,
            cache_hit,
            similarity,
            route,
            model,
            input_tokens,
            output_tokens,
            cost,
            latency_ms
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        query,
        cache_hit,
        similarity,
        route,
        model,
        input_tokens,
        output_tokens,
        cost,
        latency_ms
    ))

    connection.commit()
    connection.close()