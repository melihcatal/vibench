from typing import List, Dict, Any, Optional
import numpy as np


class EmbeddingRequest:
    """Normalize input for Cohere Embeddings API."""

    def __init__(self, texts: List[str], input_type: str = "search_document"):
        self.texts = texts
        self.input_type = input_type
        self.model = "embed-english-v3.0"
        self.truncate = "END"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "texts": self.texts,
            "model": self.model,
            "input_type": self.input_type,
            "truncate": self.truncate,
        }


class EmbeddingResponse:
    """Parse and normalize Cohere Embeddings API response."""

    def __init__(self, response: Dict[str, Any]):
        self.response = response
        self.embeddings = response.get("embeddings", [])

    def get_embeddings(self) -> List[List[float]]:
        return [embedding for embedding in self.embeddings]

    def get_normalized_embeddings(self) -> List[List[float]]:
        return [self._normalize(embedding) for embedding in self.embeddings]

    def _normalize(self, embedding: List[float]) -> List[float]:
        arr = np.array(embedding, dtype=np.float32)
        norm = np.linalg.norm(arr)
        if norm == 0:
            return arr.tolist()
        return (arr / norm).tolist()