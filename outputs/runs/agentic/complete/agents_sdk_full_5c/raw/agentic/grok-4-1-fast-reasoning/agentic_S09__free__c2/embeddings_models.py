import numpy as np
from typing import List

def normalize_embedding(embedding: List[float]) -> np.ndarray:
    arr = np.array(embedding, dtype=np.float32)
    norm = np.linalg.norm(arr)
    return arr / norm if norm > 0 else arr

def cosine_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
    return float(np.dot(emb1, emb2))