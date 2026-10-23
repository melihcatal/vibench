from typing import List
from observability_client import initialize_vertex_ai
from vertexai.language_models import TextEmbeddingModel


def embed_log_messages(log_messages: List[str]) -> List[List[float]]:
    initialize_vertex_ai()
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = model.get_embeddings(log_messages)

    return [embedding.values for embedding in embeddings]


if __name__ == "__main__":
    sample_logs = [
        "User authentication failed for user 'admin'.",
        "Database connection timeout.",
        "Payment processed successfully for order '12345'.",
        "User 'guest' logged in.",
        "Failed to connect to the primary database server.",
    ]

    log_embeddings = embed_log_messages(sample_logs)

    for message, embedding in zip(sample_logs, log_embeddings):
        print(f"Log: {message}")
        print(f"Embedding vector length: {len(embedding)}")
        print(f"Embedding (first 5 values): {embedding[:5]}")
        print("-" * 20)
