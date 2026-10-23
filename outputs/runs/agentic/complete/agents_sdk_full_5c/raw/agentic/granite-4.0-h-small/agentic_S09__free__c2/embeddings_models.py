# embeddings_models.py
import os
import json
from typing import Any, Dict

def check_response(resp: Dict[str, Any]) -> None:
    """Validate Direct Embeddings API response and raise if invalid.

    Args:
        resp (Dict[str, Any]): raw API response from Direct Embeddings.

    Raises:
        ValueError: if response indicates error or missing data.
    """
    if 'error' in resp and resp['error']:
        raise ValueError(f"Embedding API error: {resp['error']}")
    if 'data' not in resp or not isinstance(resp['data'], list):
        raise ValueError("Unexpected response format: missing 'data' list")
    # Basic normalization: ensure embeddings are lists of floats
    for item in resp['data']:
        if 'embedding' not in item or not isinstance(item['embedding'], list):
            raise ValueError("Embedding missing or not a list")
        # Cast to float for safety
        item['embedding'] = [float(v) for v in item['embedding']]


def normalize_embedding(embedding: list[float]) -> list[float]:
    """Return a normalized (unit-length) embedding vector.

    Args:
        embedding (list[float]): raw embedding.

    Returns:
        list[float]: normalized embedding.
    """
    arr = np.array(embedding)
    norm = np.linalg.norm(arr)
    if norm == 0:
        raise ValueError("Zero-length embedding vector")
    return (arr / norm).tolist()

# Export numpy for helpers that need it
import numpy as np
