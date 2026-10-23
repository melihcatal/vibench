from embeddings_client import DirectEmbeddingsClient

# OpenAI Embeddings provider
client = DirectEmbeddingsClient(service="OpenAI")


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        vec1 (list[float]): First embedding vector.
        vec2 (list[float]): Second embedding vector.
    Returns:
        float: Cosine similarity score in range [-1, 1].
    """
    # Basic cosine similarity without using external libraries
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a * a for a in vec1) ** 0.5
    norm2 = sum(b * b for b in vec2) ** 0.5
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def similarity_score(text1: str, text2: str) -> float:
    """Compute similarity between two texts using embeddings.

    Args:
        text1 (str): First text.
        text2 (str): Second text.
    Returns:
        float: Similarity score.
    """
    emb1 = client.embed(text=text1)
    emb2 = client.embed(text=text2)
    return cosine_similarity(emb1, emb2)
