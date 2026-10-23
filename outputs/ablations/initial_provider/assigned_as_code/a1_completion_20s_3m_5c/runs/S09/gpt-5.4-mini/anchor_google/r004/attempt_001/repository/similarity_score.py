from embeddings_models import cosine_similarity


def similarity_score(payload, config=None):
    return {"similarity": cosine_similarity(payload["embedding_a"], payload["embedding_b"])}
