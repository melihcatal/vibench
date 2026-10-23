import numpy as np
from typing import List

def normalize_embedding(embedding: List[float]) -> np.ndarray:
    emb = np.array(embedding, dtype=np.float32)
    norm = np.linalg.norm(emb)
    if norm == 0:
        return emb
    return emb / norm

def cosine_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
    return np.dot(emb1, emb2)
