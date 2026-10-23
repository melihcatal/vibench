from typing import List, Dict, Any, Optional
import numpy as np


class EmbeddingRequest:
    """Request payload for embeddings."""

    def __init__(self, texts: List[str], truncate_input_tokens: Optional[int] = None):
        self.texts = texts
        self.truncate_input_tokens = truncate_input_tokens

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary."""
        payload = {"input": self.texts}
        if self.truncate_input_tokens:
            payload["truncate_input_tokens"] = self.truncate_input_tokens
        return payload


class EmbeddingResponse:
    """Response payload for embeddings."""

    def __init__(self, data: List[Dict[str, Any]], model_id: str):
        self.data = data
        self.model_id = model_id

    def get_embeddings(self) -> List[List[float]]:
        """Extract embeddings from response."""
        return [item["embedding"] for item in self.data]

    def get_normalized_embeddings(self) -> List[List[float]]:
        """Extract and normalize embeddings."""
        embeddings = self.get_embeddings()
        return [self._normalize(embedding) for embedding in embeddings]

    def _normalize(self, embedding: List[float]) -> List[float]:
        """Normalize embedding to unit length."""
        arr = np.array(embedding, dtype=np.float32)
        norm = np.linalg.norm(arr)
        return (arr / norm).tolist()
