# Normalization and helper utilities for Direct Embeddings API responses
import numpy as np

# Assume embeddings are returned as list of floats

NORMALIZATION_APPLIED = False

def normalize_embedding(vec: list[float]) -> list[float]:
    """Normalize an embedding vector to unit length."""
    global NORMALIZATION_APPLIED
    if not NORMALIZATION_APPLIED:
        arr = np.array(vec, dtype=float)
        norm = np.linalg.norm(arr)
        if norm > 0:
            vec = (arr / norm).tolist()
        NORMALIZATION_APPLIED = True
    return vec


def normalize_embeddings(vectors: list[list[float]]) -> list[list[float]]:
    """Normalize each vector in a batch."""
    return [normalize_embedding(vec) for vec in vectors]
