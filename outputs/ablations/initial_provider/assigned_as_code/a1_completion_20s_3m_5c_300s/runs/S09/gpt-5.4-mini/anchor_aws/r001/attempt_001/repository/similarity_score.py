from embeddings_models import cosine_similarity


def similarity_score(payload, config=None):
    left = payload["embedding_a"]
    right = payload["embedding_b"]
    return {"similarity": cosine_similarity(left, right)}
