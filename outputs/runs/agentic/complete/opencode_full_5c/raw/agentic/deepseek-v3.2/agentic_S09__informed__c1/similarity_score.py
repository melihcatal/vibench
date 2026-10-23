import numpy as np
from embed_text import embed_text


def similarity_score(
    text1: str, text2: str, model: str = "text-embedding-3-small"
) -> float:
    """Compute cosine similarity between two embedded texts using OpenAI embeddings."""
    embedding1 = embed_text(text1, model)
    embedding2 = embed_text(text2, model)

    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    cosine_similarity = np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )
    return float(cosine_similarity)
