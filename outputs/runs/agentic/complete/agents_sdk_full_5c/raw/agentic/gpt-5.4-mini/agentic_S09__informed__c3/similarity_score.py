from embed_text import embed_text
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str) -> float:
    embedding_a = embed_text(text_a)
    embedding_b = embed_text(text_b)
    return cosine_similarity(embedding_a, embedding_b)
