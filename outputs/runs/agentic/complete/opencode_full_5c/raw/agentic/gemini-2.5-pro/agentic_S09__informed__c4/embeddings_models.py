from typing import List
import numpy as np


class EmbeddingResponse:
    def __init__(self, text: str, embedding: List[float]):
        self.text = text
        self.embedding = embedding


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
