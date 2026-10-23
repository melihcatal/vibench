from embeddings_models import cosine_similarity
from embed_text import embed_text


def similarity_score(left_text: str, right_text: str) -> float:
    left = embed_text(left_text).vector
    right = embed_text(right_text).vector
    return cosine_similarity(left, right)
