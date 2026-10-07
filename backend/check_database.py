import sqlite3


connection = sqlite3.connect("metrics.db")

cursor = connection.cursor()

cursor.execute("""
    SELECT
        id,
        query,
        cache_hit,
        route,
        model,
        cost,
        latency_ms
    FROM requests
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()