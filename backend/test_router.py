from app.router import route_query


queries = [
    "What is Python?",
    "What is machine learning?",
    "Compare Python and Java and explain their advantages and disadvantages.",
    "Why does machine learning require data?"
]


for query in queries:
    result = route_query(query)

    print("\nQuery:", query)
    print("Route:", result["route"])
    print("Model:", result["model"])