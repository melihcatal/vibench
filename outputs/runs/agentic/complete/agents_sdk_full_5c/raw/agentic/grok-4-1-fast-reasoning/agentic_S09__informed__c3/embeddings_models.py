import numpy as np
from typing import List

def extract_embeddings(response) -> List[List[float]]:
    return [data.embedding for data in response.data]

def cosine_similarity(a: List[float], b: List[float]) -> float:
    aa = np.array(a)
    bb = np.array(b)
    return np.dot(aa, bb) / (np.linalg.norm(aa) * np.linalg.norm(bb))