from typing import List, Dict, Any, Optional
import numpy as np


class EmbeddingRequest:
    """Normalize input text for Cohere Embed API."""
    
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
    """Parse and normalize Cohere Embed API response."""
    
    def __init__(self, response: Dict[str, Any]):
        self.response = response
        self.embeddings = response.get("embeddings", [])
        self.meta = response.get("meta", {})

    def get_embeddings(self) -> List[List[float]]:
        """Return embeddings as a list of lists of floats."""
        return [embedding for embedding in self.embeddings]

    def get_normalized_embeddings(self) -> List[List[float]]:
        """Return L2-normalized embeddings."""
        embeddings = self.get_embeddings()
        return [self._normalize(embedding) for embedding in embeddings]

    def _normalize(self, embedding: List[float]) -> List[float]:
        """L2-normalize a single embedding."""
        arr = np.array(embedding, dtype=np.float32)
        norm = np.linalg.norm(arr)
        if norm == 0:
            return arr.tolist()
        return (arr / norm).tolist()