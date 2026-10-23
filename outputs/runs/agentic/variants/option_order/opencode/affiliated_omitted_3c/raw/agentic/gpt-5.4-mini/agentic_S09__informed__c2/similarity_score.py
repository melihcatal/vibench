from embed_text import embed_text
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str) -> float:
    emb_a = embed_text(text_a)
    emb_b = embed_text(text_b)
    return cosine_similarity(emb_a, emb_b)
