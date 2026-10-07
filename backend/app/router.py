def route_query(query: str):
    """
    Decide which model should handle the query.
    """

    query_lower = query.lower()

    complex_keywords = [
        "analyze",
        "analyse",
        "compare",
        "difference",
        "explain in detail",
        "reason",
        "evaluate",
        "advantages and disadvantages",
        "pros and cons",
        "step by step",
        "why",
        "how does",
    ]

    for keyword in complex_keywords:
        if keyword in query_lower:
            return {
                "model": "openai/gpt-oss-120b",
                "route": "large"
            }

    # Long queries are treated as more complex
    if len(query.split()) > 30:
        return {
            "model": "openai/gpt-oss-120b",
            "route": "large"
        }

    # Default: use the cheaper/smaller model
    return {
        "model": "openai/gpt-oss-20b",
        "route": "small"
    }