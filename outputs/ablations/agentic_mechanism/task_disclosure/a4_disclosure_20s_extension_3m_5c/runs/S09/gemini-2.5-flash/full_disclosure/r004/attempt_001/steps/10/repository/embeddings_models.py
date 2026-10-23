import numpy as np
from typing import List, Dict, Any

class EmbeddingRequest:
    """
    Represents a request to the Direct Embeddings API.
    """
    def __init__(self, text: str):
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text}

class EmbeddingResponse:
    """
    Represents a response from the Direct Embeddings API, containing an embedding vector.
    """
    def __init__(self, embedding: List[float]):
        self.embedding = np.array(embedding)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data["embedding"])

    def to_list(self) -> List[float]:
        return self.embedding.tolist()

def normalize_embedding(embedding: np.ndarray) -> np.ndarray:
    """
    Normalizes an embedding vector to unit length.
    """
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return embedding / norm
