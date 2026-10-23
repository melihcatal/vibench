from embeddings_models import cosine_similarity
from embed_text import embed_text


def similarity_score(text_a: str, text_b: str) -> float:
    return cosine_similarity(embed_text(text_a), embed_text(text_b))
