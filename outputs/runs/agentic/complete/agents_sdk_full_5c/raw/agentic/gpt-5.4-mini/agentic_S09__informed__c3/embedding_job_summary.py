from collections import Counter
from statistics import mean

from embeddings_models import cosine_similarity
from embed_batch import embed_batch


def embedding_job_summary(texts: list[str]) -> dict[str, object]:
    vectors = embed_batch(texts)
    dimensions = [len(vector) for vector in vectors]
    pairwise = [
        cosine_similarity(vectors[i], vectors[j])
        for i in range(len(vectors))
        for j in range(i + 1, len(vectors))
    ]
    return {
        "count": len(vectors),
        "dimension_mode": Counter(dimensions).most_common(1)[0][0] if dimensions else 0,
        "average_dimension": mean(dimensions) if dimensions else 0.0,
        "average_pairwise_similarity": mean(pairwise) if pairwise else 0.0,
        "provider": "cohere",
        "model": __import__("embeddings_client").get_model(),
    }
