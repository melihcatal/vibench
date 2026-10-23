import numpy as np

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors.
    """
    a = np.array(vec1, dtype=np.float32)
    b = np.array(vec2, dtype=np.float32)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
