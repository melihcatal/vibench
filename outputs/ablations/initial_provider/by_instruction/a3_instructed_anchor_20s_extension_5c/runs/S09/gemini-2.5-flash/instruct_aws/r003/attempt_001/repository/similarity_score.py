import numpy as np
from embeddings_models import EmbeddingResult

def cosine_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    """Computes the cosine similarity between two embedding vectors.

    Args:
        embedding1: The first embedding vector.
        embedding2: The second embedding vector.

    Returns:
        The cosine similarity score.
    """
    dot_product = np.dot(embedding1, embedding2)
    norm_a = np.linalg.norm(embedding1)
    norm_b = np.linalg.norm(embedding2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def similarity_score(embedding_result1: EmbeddingResult, embedding_result2: EmbeddingResult) -> float:
    """Computes the cosine similarity between two embedded texts.

    Args:
        embedding_result1: The first EmbeddingResult object.
        embedding_result2: The second EmbeddingResult object.

    Returns:
        The cosine similarity score.
    """
    return cosine_similarity(embedding_result1.embedding, embedding_result2.embedding)
