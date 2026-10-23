import math
from embed_text import embed_text
from embeddings_client import DEFAULT_EMBEDDING_MODEL


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def similarity_score(
    text_a: str, text_b: str, model: str = DEFAULT_EMBEDDING_MODEL
) -> float:
    vec_a = embed_text(text_a, model=model)
    vec_b = embed_text(text_b, model=model)
    return cosine_similarity(vec_a, vec_b)
