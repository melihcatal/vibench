from typing import List


def normalize_embedding(embedding: List[float]) -> List[float]:
    return [float(x) for x in embedding]
