from embeddings_models import cosine_similarity


def embedding_job_summary(payload, config=None):
    embeddings = payload["embeddings"]
    count = len(embeddings)
    dimensions = len(embeddings[0]) if embeddings else 0
    centroid = [sum(values) / count for values in zip(*embeddings)] if embeddings else []
    return {"count": count, "dimensions": dimensions, "centroid": centroid, "average_self_similarity": cosine_similarity(centroid, centroid) if centroid else 0.0}
