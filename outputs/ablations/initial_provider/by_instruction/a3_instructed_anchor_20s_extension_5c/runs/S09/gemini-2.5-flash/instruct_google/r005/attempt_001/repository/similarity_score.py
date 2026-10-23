import math

def similarity_score(embedding1: list[float], embedding2: list[float]) -> float:
    """Computes the cosine similarity between two embedding vectors.

    Args:
        embedding1: The first embedding vector.
        embedding2: The second embedding vector.

    Returns:
        The cosine similarity score.
    """
    dot_product = sum(e1 * e2 for e1, e2 in zip(embedding1, embedding2))
    magnitude1 = math.sqrt(sum(e1 * e1 for e1 in embedding1))
    magnitude2 = math.sqrt(sum(e2 * e2 for e2 in embedding2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)
