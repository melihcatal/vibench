import numpy as np
from typing import List, Union

def normalize_embedding(embedding: Union[List[float], np.ndarray]) -> np.ndarray:
    emb = np.array(embedding)
    norm = np.linalg.norm(emb)
    return emb / norm if norm != 0 else emb

def cosine_similarity(emb1: Union[List[float], np.ndarray], emb2: Union[List[float], np.ndarray]) -> float:
    emb1_norm = normalize_embedding(emb1)
    emb2_norm = normalize_embedding(emb2)
    return float(np.dot(emb1_norm, emb2_norm))