from typing import List, Dict, Any


def normalize_embedding_response(response: Any) -> List[List[float]]:
    """Normalizes the embedding response from the API."""
    embeddings = []
    if hasattr(response, "embeddings"):
        for embedding_obj in response.embeddings:
            embeddings.append(embedding_obj.values)
    return embeddings


def create_embedding_request_payload(texts: List[str]) -> Dict[str, Any]:
    """Creates a payload for an embedding request."""
    return {
        "texts": texts,
        "model": "embedding-001",  # This might be overridden by the client, but good for local def
    }
