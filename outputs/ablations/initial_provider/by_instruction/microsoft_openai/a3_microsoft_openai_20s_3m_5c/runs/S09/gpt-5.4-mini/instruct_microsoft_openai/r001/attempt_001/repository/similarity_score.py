from embeddings_client import embed_single_text
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str):
    return cosine_similarity(embed_single_text(text_a), embed_single_text(text_b))
