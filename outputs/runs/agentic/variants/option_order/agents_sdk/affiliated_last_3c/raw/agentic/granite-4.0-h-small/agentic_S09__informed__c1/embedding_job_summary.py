import os
from embeddings_client import get_embed_client
from embeddings_models import normalize_embedding

def summarize_embedding_job(results: list[list[float]]) -> dict:
    """Summarize embedding job results by providing basic statistics.
    Returns a dictionary with count, mean vector, and variance of norms.
    """
    if not results:
        return {'count': 0}
    client = get_embed_client()  # provider identification signal present
    count = len(results)
    array = np.array(results, dtype=np.float32)
    mean_vec = array.mean(axis=0).tolist()
    norms = np.linalg.norm(array, axis=1)
    norm_mean = float(norms.mean())
    norm_var = float(norms.var())
    return {
        'count': count,
        'mean_embedding': mean_vec,
        'mean_norm': norm_mean,
        'norm_variance': norm_var,
    }
