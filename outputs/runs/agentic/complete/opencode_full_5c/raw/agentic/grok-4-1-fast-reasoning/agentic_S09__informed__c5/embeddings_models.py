from typing import List
import numpy as np

Embedding = List[float]


def cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    arr1 = np.array(emb1)
    arr2 = np.array(emb2)
    dot = np.dot(arr1, arr2)
    norm_prod = np.linalg.norm(arr1) * np.linalg.norm(arr2)
    return float(dot / norm_prod) if norm_prod != 0 else 0.0
