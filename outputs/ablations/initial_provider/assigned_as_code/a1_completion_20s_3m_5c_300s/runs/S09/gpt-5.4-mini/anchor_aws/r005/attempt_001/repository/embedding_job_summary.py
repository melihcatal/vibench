from embeddings_models import cosine_similarity


def embedding_job_summary(payload, config=None):
    embeddings = payload.get("embeddings", [])
    total = len(embeddings)
    average_dimension = sum(len(item) for item in embeddings) / total if total else 0
    return {"total_embeddings": total, "average_dimension": average_dimension, "pairwise_similarity": cosine_similarity(embeddings[0], embeddings[1]) if total >= 2 else 0.0}
