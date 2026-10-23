from embeddings_models import cosine_similarity


def similarity_score(payload, config=None):
    left = payload["left_embedding"]
    right = payload["right_embedding"]
    return {"similarity": cosine_similarity(left, right)}
