from typing import List


def normalize_embedding(embedding: List[float]) -> List[float]:
    norm_value = sum(val**2 for val in embedding) ** 0.5
    return [val / norm_value for val in embedding]
