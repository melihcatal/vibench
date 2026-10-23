import numpy as np
from typing import List, Dict, Any


def normalize_embedding(embedding: List[float]) -> np.ndarray:
    """Normalizes an embedding vector to a NumPy array."""
    return np.array(embedding).flatten()


def prepare_text_for_embedding(text: str) -> Dict[str, Any]:
    """Prepares a single text string for the embedding API."""
    return {"text": text}


def prepare_batch_for_embedding(texts: List[str]) -> Dict[str, Any]:
    """Prepares a batch of text strings for the embedding API."""
    return {"texts": texts}


def parse_embedding_response(response: Any) -> List[float]:
    """Parses the embedding response from the API."""
    # Assuming the response object has an 'embedding' attribute or similar
    if hasattr(response, "embedding") and hasattr(response.embedding, "values"):
        return response.embedding.values
    raise ValueError("Invalid embedding response format.")


def parse_batch_embedding_response(response: Any) -> List[List[float]]:
    """Parses a batch embedding response from the API."""
    if hasattr(response, "embeddings"):
        return [emb.values for emb in response.embeddings]
    raise ValueError("Invalid batch embedding response format.")
