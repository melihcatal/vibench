# embeddings_models.py
# HELPER
import numpy as np

def normalize_embedding(embedding: list) -> np.ndarray:
    """Convert list embedding to unit L2 vector."""
    arr = np.array(embedding, dtype=np.float32)
    norm = np.linalg.norm(arr)
    if norm == 0:
        raise ValueError("Zero vector cannot be normalized")
    return arr / norm
