from app.embedding import create_embedding, calculate_similarity


query1 = "What is machine learning?"
query2 = "Explain machine learning."
query3 = "What is the capital of France?"


embedding1 = create_embedding(query1)
embedding2 = create_embedding(query2)
embedding3 = create_embedding(query3)


similarity_1 = calculate_similarity(
    embedding1,
    embedding2
)

similarity_2 = calculate_similarity(
    embedding1,
    embedding3
)


print("Query 1:", query1)
print("Query 2:", query2)
print("Similarity:", similarity_1)

print()

print("Query 1:", query1)
print("Query 3:", query3)
print("Similarity:", similarity_2)