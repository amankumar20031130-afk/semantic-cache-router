from app.embedding import create_embedding

text = "What is machine learning?"

embedding = create_embedding(text)

print("Embedding size:", len(embedding))
print("First 5 values:", embedding[:5])