import os
from typing import List


def normalize_embedding(vector: List[float]) -> List[float]:
    """L2-normalize an embedding vector (list of floats)."""
    arr = np.array(vector, dtype=np.float32)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return vector  # zero vector remains unchanged
    return (arr / norm).tolist()


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors (lists)."""
    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)
    if a.shape != b.shape:
        raise ValueError("Dimension mismatch between embeddings")
    norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))