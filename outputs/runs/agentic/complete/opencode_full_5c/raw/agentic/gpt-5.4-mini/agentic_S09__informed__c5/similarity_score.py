from embeddings_client import embed_texts
from embeddings_models import cosine_similarity


def similarity_score(left_text: str, right_text: str) -> float:
    left, right = embed_texts([left_text, right_text])
    return cosine_similarity(left, right)
