from embeddings_models import cosine_similarity
from embed_text import embed_text


def similarity_score(left_text: str, right_text: str) -> float:
    left_vec = embed_text(left_text).vectors[0]
    right_vec = embed_text(right_text).vectors[0]
    return cosine_similarity(left_vec, right_vec)
