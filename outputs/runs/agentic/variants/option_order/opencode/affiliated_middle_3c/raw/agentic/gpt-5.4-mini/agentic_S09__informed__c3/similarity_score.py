from math import sqrt
from embed_text import embed_text


def cosine_similarity(text_a: str, text_b: str):
    vec_a = embed_text(text_a)
    vec_b = embed_text(text_b)
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sqrt(sum(a * a for a in vec_a))
    norm_b = sqrt(sum(b * b for b in vec_b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0
