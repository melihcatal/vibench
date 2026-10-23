from typing import List, Dict, Any, Optional
import numpy as np


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalize embedding vector to unit length."""
    arr = np.array(embedding, dtype=np.float32)
    norm = np.linalg.norm(arr)
    return (arr / norm).tolist()


def parse_embedding_response(response: Dict[str, Any]) -> List[float]:
    """Parse embedding vector from OpenAI API response."""
    return response["data"][0]["embedding"]


def parse_batch_embedding_response(response: Dict[str, Any]) -> List[List[float]]:
    """Parse batch embedding vectors from OpenAI API response."""
    return [item["embedding"] for item in response["data"]]