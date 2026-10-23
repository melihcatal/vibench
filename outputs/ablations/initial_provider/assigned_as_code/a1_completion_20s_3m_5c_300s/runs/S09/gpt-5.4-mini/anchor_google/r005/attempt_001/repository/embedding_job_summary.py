from embeddings_models import cosine_similarity


def embedding_job_summary(payload, config=None):
    embeddings = payload["embeddings"]
    return {"count": len(embeddings), "first_pair_similarity": cosine_similarity(embeddings[0], embeddings[1]) if len(embeddings) > 1 else 0.0}
