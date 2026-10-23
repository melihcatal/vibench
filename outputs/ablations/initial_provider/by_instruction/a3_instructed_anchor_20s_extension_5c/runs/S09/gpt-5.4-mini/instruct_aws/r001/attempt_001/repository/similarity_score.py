from embeddings_models import cosine_similarity
from embed_text import embed_text


def similarity_score(text_a, text_b):
    return cosine_similarity(embed_text(text_a), embed_text(text_b))
