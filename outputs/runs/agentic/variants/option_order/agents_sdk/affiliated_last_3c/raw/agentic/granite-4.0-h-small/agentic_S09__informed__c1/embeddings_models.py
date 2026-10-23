import os
import numpy as np
from typing import List, Any

# Provider identification signal: using OpenAI SDK for normalization example.
# Other providers can be normalized similarly (e.g., length check, scaling).

def normalize_embedding(vec: List[float]) -> List[float]:
    """Normalize an embedding vector to unit length.
    Returns a new list of floats.
    """
    arr = np.array(vec, dtype=np.float32)
    norm = np.linalg.norm(arr)
    if norm == 0:
        # Return zero vector if input is zero to avoid division by zero
        return vec
    return (arr / norm).tolist()


def normalize_embedding_batch(batch: List[List[float]]) -> List[List[float]]:
    """Normalize each vector in a batch of embeddings.
    Returns a new list of lists.
    """
    return [normalize_embedding(v) for v in batch]
