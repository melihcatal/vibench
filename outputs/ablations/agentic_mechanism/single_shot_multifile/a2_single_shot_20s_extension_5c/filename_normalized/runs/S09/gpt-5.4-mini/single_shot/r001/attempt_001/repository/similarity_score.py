import math
from embed_text import embed_text


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def similarity_score(text_a: str, text_b: str, model: str | None = None) -> float:
    emb_a = embed_text(text_a, model=model)
    emb_b = embed_text(text_b, model=model)
    return cosine_similarity(emb_a, emb_b)
