from embeddings_models import cosine_similarity
from embed_text import embed_text


def similarity_score(text_a: str, text_b: str) -> float:
    left = embed_text(text_a).embedding
    right = embed_text(text_b).embedding
    return cosine_similarity(left, right)
