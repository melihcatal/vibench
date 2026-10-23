from math import sqrt

from embeddings_client import embed_texts


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def similarity_score(text_a: str, text_b: str) -> float:
    left, right = embed_texts([text_a, text_b])
    return cosine_similarity(left, right)
