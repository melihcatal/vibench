from embeddings_models import cosine_similarity


def similarity_score(payload, config=None):
    return {"similarity": cosine_similarity(payload["left_embedding"], payload["right_embedding"])}
