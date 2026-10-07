from app.embedding import create_embedding, calculate_similarity


class SemanticCache:
    def __init__(self, similarity_threshold=0.70):
        self.cache = []
        self.similarity_threshold = similarity_threshold

    def find(self, query: str):
        if not self.cache:
            return None

        query_embedding = create_embedding(query)

        best_match = None
        best_similarity = 0

        for item in self.cache:
            similarity = calculate_similarity(
                query_embedding,
                item["embedding"]
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = item

        return {
            "answer": best_match["answer"],
            "similarity": float(best_similarity),
            "cache_hit": best_similarity >= self.similarity_threshold
        }

    def add(self, query: str, answer: str):
        embedding = create_embedding(query)

        self.cache.append({
            "query": query,
            "embedding": embedding,
            "answer": answer
        })