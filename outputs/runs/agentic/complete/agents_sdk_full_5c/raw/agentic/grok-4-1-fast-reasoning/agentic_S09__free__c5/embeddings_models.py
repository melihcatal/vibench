from typing import List

MODEL_ID = "text-embedding-3-small"

def normalize_embedding(embedding: List[float]) -> List[float]:
    norm_sq = sum(x * x for x in embedding)
    if norm_sq == 0:
        return embedding
    norm = norm_sq ** 0.5
    return [x / norm for x in embedding]