# embeddings_models.py
# [HELPER] Request, response, and normalization helpers for Direct Embeddings API

import json
from typing import List, Any


def normalize_embedding(embedding: Any) -> List[float]:
    """Ensure embedding is a list of floats."""
    if isinstance(embedding, (list, tuple)):
        return [float(x) for x in embedding]
    raise ValueError("Embedding must be a list or tuple of numbers")


# Example: structure of an embeddings API response (WatsonX)
# [{"text": "sample", "embedding": [0.1, 0.2, ...]}]


def parse_response(response_json: str) -> List[List[float]]:
    """Parse JSON response and return list of embedding vectors."""
    data = json.loads(response_json)
    # Assume response contains a list under a "results" key (adjust per provider)
    embeddings = []
    for item in data.get("results", []):
        embedding = item.get("embedding")
        if embedding:
            embeddings.append(normalize_embedding(embedding))
    return embeddings
