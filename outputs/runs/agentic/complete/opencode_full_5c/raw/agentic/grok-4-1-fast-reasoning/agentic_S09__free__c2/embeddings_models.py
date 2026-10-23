from typing import List
from dataclasses import dataclass


@dataclass
class Embedding:
    text: str
    vector: List[float]


def l2_normalize(embedding: List[float]) -> List[float]:
    norm = sum(x**2 for x in embedding) ** 0.5
    if norm == 0:
        return embedding[:]
    return [x / norm for x in embedding]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x**2 for x in a) ** 0.5
    norm_b = sum(y**2 for y in b) ** 0.5
    return dot_product / (norm_a * norm_b) if norm_a * norm_b > 0 else 0.0
