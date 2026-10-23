from embeddings_client import embed_text_google
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str) -> float:
    embedding_a = embed_text_google(text_a)
    embedding_b = embed_text_google(text_b)
    return cosine_similarity(embedding_a, embedding_b)
