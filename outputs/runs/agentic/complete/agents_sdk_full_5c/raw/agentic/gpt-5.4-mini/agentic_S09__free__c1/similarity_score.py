import math

from embed_text import embed_text


def cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


def similarity_score(text_a: str, text_b: str):
    embedding_a = embed_text(text_a)
    embedding_b = embed_text(text_b)
    return cosine_similarity(embedding_a, embedding_b)
