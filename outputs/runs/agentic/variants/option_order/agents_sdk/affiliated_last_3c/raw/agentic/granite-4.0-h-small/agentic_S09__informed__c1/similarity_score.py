import numpy as np
from embeddings_models import normalize_embedding

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.
    Both vectors are assumed to be normalized; normalization is enforced for safety.
    """
    a = np.array(normalize_embedding(vec_a), dtype=np.float32)
    b = np.array(normalize_embedding(vec_b), dtype=np.float32)
    return float(np.dot(a, b))
