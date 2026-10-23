# embedding_job_summary.py
# LATER-STEP
from embeddings_models import normalize_embedding
import numpy as np

def summarize(job_results: list) -> dict:
    """Summarize a list of embedding job results.

    Args:
        job_results: list of dicts with keys 'text', 'embedding' (list).
    Returns:
        Dict with total count, list of normalized embeddings, and average vector length.
    """
    embeddings = []
    lengths = []
    for r in job_results:
        vec = normalize_embedding(r['embedding'])
        embeddings.append(vec)
        lengths.append(np.linalg.norm(vec))
    avg_length = sum(lengths) / len(lengths) if lengths else 0.0
    return {
        "count": len(job_results),
        "average_vector_length": avg_length,
        "embeddings": [vec.tolist() for vec in embeddings]  # JSON serializable
    }
