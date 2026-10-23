import numpy as np
from typing import List

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536

def cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    a = np.array(emb1)
    b = np.array(emb2)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def normalize_embedding(emb: List[float]) -> np.ndarray:
    arr = np.array(emb)
    return arr / np.linalg.norm(arr)
