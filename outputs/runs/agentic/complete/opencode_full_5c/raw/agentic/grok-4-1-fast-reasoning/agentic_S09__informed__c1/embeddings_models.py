from typing import List
import math


def normalize_texts(texts: List[str]) -> List[str]:
    return [text.strip() for text in texts if text.strip()]


def normalize_embedding(embedding: List[float]) -> List[float]:
    norm = math.sqrt(sum(x * x for x in embedding))
    return [x / norm for x in embedding] if norm > 0 else embedding


def cosine_similarity(a: List[float], b: List[float]) -> float:
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (norm_a * norm_b)
