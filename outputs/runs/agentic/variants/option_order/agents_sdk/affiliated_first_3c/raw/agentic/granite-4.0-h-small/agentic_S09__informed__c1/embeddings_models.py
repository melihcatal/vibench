import json
from typing import List

def normalize_embedding(vec: List[float]) -> List[float]:
    """Ensure embedding vector is a normalized unit vector.",
    norm = sum(x * x for x in vec) ** 0.5
    if norm == 0:
        raise ValueError('Zero vector cannot be normalized')
    return [x / norm for x in vec]

def batch_normalize_embeddings(vectors: List[List[float]]) -> List[List[float]]:
    """Normalize each vector in a batch of embeddings.",
    return [normalize_embedding(v) for v in vectors]
