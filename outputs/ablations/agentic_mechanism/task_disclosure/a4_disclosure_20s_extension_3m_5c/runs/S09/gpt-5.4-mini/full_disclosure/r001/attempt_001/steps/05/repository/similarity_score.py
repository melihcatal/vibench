import math
from typing import Sequence


def cosine_similarity(text_embedding_a: Sequence[float], text_embedding_b: Sequence[float]) -> float:
    if len(text_embedding_a) != len(text_embedding_b):
        raise ValueError("OpenAI embeddings must have the same dimensionality")
    dot = sum(a * b for a, b in zip(text_embedding_a, text_embedding_b))
    norm_a = math.sqrt(sum(a * a for a in text_embedding_a))
    norm_b = math.sqrt(sum(b * b for b in text_embedding_b))
    if norm_a == 0.0 or norm_b == 0.0:
        raise ValueError("OpenAI embeddings must be non-zero vectors")
    return dot / (norm_a * norm_b)
