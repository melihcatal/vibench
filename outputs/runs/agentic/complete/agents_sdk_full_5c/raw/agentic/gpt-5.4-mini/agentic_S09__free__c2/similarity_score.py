import math

from embed_text import embed_text


def cosine_similarity(text_a: str, text_b: str) -> float:
    vec_a = embed_text(text_a)
    vec_b = embed_text(text_b)
    numerator = sum(a * b for a, b in zip(vec_a, vec_b))
    denom_a = math.sqrt(sum(a * a for a in vec_a))
    denom_b = math.sqrt(sum(b * b for b in vec_b))
    if denom_a == 0.0 or denom_b == 0.0:
        return 0.0
    return numerator / (denom_a * denom_b)
