from embeddings_models import cosine_similarity
from embed_text import embed_text


def similarity_score(text_a: str, text_b: str) -> float:
    emb_a = embed_text(text_a).vector
    emb_b = embed_text(text_b).vector
    return cosine_similarity(emb_a, emb_b)
