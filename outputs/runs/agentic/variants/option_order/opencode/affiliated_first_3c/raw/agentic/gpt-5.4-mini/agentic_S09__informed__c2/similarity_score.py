from embeddings_models import cosine_similarity, normalize_vector
from embed_text import embed_text


def similarity_score(text_a: str, text_b: str) -> float:
    emb_a = normalize_vector(embed_text(text_a).vector)
    emb_b = normalize_vector(embed_text(text_b).vector)
    return cosine_similarity(emb_a, emb_b)
