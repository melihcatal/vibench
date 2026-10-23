# embeddings_models.py
from typing import List

def normalize_embedding(vec: List[float]) -> List[float]:
    """L2‑normalize an embedding vector.",
    norm = sum(x * x for x in vec) ** 0.5
    if norm == 0:
        return vec
    return [x / norm for x in vec]