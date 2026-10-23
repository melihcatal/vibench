from embeddings_models import cosine_similarity, normalize_vector


def similarity_score(left_embedding, right_embedding):
    return cosine_similarity(normalize_vector(left_embedding), normalize_vector(right_embedding))
