import numpy as np
from embed_text import embed_text
from embeddings_models import normalize_embedding


def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Computes the cosine similarity between two embedding vectors."""
    dot_product = np.dot(embedding1, embedding2)
    norm_a = np.linalg.norm(embedding1)
    norm_b = np.linalg.norm(embedding2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def similarity_score(
    text1: str, text2: str, model_name: str = "models/embedding-001"
) -> float:
    """Computes the cosine similarity between two text strings using their Gemini embeddings.

    Args:
        text1: The first text string.
        text2: The second text string.
        model_name: The name of the embedding model to use.

    Returns:
        The cosine similarity score between the embeddings of the two texts.
    """
    embedding1_raw = embed_text(text1, model_name)
    embedding2_raw = embed_text(text2, model_name)

    embedding1 = normalize_embedding(embedding1_raw)
    embedding2 = normalize_embedding(embedding2_raw)

    return cosine_similarity(embedding1, embedding2)
