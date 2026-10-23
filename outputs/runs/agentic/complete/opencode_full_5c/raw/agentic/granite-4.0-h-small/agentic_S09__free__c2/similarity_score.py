import numpy as np
from embeddings_client import DirectEmbeddingsClient


def similarity_score(embed_a: list[float], embed_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        embed_a: First embedding vector.
        embed_b: Second embedding vector.

    Returns:
        Cosine similarity score (float between -1 and 1).
    """
    a = np.array(embed_a)
    b = np.array(embed_b)
    # Cosine similarity = dot(a, b) / (||a|| * ||b||)
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)
