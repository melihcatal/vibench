from typing import Dict, List

from embeddings_client import DirectEmbeddingsClient


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalize the embedding vector to unit length."""
    import numpy as np
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return [float(x) / norm for x in embedding]


def prepare_embedding_request(texts: List[str]) -> Dict:
    """Prepare the request payload for the Direct Embeddings API."""
    return {
        'texts': texts,
        'model': DirectEmbeddingsClient.MODEL_NAME
    }


def process_embedding_response(response: Dict) -> List[List[float]]:
    """Process the response from the Direct Embeddings API."""
    embeddings = response.get('embeddings', [])
    return [normalize_embedding(emb) for emb in embeddings]