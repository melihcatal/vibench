import embeddings_client

# Direct Embeddings API integration (example provider: OpenAI)


def similarity_score(embedding_a: list, embedding_b: list) -> float:
    """Compute cosine similarity between two embedding vectors.
    Returns a float between -1 and 1.
    """
    client = embeddings_client.EmbeddingsClient()  # not used directly here
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = sum(a * a for a in embedding_a) ** 0.5
    norm_b = sum(b * b for b in embedding_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)
