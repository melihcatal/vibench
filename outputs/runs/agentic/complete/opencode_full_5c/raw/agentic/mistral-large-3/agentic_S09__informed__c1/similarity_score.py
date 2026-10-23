import numpy as np
from typing import List


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Compute cosine similarity between two embeddings."""
    arr1 = np.array(embedding1, dtype=np.float32)
    arr2 = np.array(embedding2, dtype=np.float32)
    return float(np.dot(arr1, arr2) / (np.linalg.norm(arr1) * np.linalg.norm(arr2)))


def similarity_score(text1: str, text2: str) -> float:
    """Compute cosine similarity between two embedded texts using IBM Slate Embeddings."""
    from embed_text import embed_text

    embedding1 = embed_text(text1)
    embedding2 = embed_text(text2)
    return cosine_similarity(embedding1, embedding2)
