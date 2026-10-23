from embeddings_models import cosine_similarity


def similarity_score(left_embedding, right_embedding):
    return cosine_similarity(left_embedding, right_embedding)
