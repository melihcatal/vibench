from typing import Dict, Any


def normalize_embedding(embedding: list[float]) -> list[float]:
    """Normalize an embedding vector to unit length."""
    import numpy as np

    vec = np.array(embedding, dtype=float)
    norm = np.linalg.norm(vec)
    if norm == 0:
        raise ValueError("Zero vector cannot be normalized")
    return (vec / norm).tolist()


def parse_response(response: Dict[str, Any]) -> Any:
    """Extract and normalize embedding from API response."""
    # Expected response shape varies by endpoint; handle accordingly
    if "embedding" in response:
        return normalize_embedding(response["embedding"])
    elif "embeddings" in response:
        return [normalize_embedding(vec) for vec in response["embeddings"]]
    else:
        raise KeyError("Response does not contain expected embedding keys")
