import statistics
from embeddings_models import EmbeddingResponse


def embedding_job_summary(embedding_response: EmbeddingResponse):
    if not embedding_response.results:
        return {
            "count": 0,
            "model": embedding_response.model,
            "avg_dimension": 0,
            "min_dimension": 0,
            "max_dimension": 0,
            "usage": embedding_response.usage,
        }

    dimensions = [len(r.embedding) for r in embedding_response.results]
    return {
        "count": len(embedding_response.results),
        "model": embedding_response.model,
        "avg_dimension": statistics.mean(dimensions),
        "min_dimension": min(dimensions),
        "max_dimension": max(dimensions),
        "avg_embedding_magnitude": statistics.mean(
            [sum(x * x for x in r.embedding) ** 0.5 for r in embedding_response.results]
        ),
        "usage": embedding_response.usage,
    }
