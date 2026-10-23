
import numpy as np
from typing import List, Dict, Any

class EmbedTextRequest:
    """
    Represents a request to the Direct Embeddings API for embedding a single text string.
    """
    def __init__(self, text: str):
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text}

class EmbedTextResponse:
    """
    Represents a response from the Direct Embeddings API containing an embedding vector.
    """
    def __init__(self, embedding: List[float]):
        self.embedding = embedding

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(embedding=data["embedding"])

def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    Normalizes an embedding vector to a unit vector (L2 normalization).
    """
    np_embedding = np.array(embedding)
    norm = np.linalg.norm(np_embedding)
    if norm == 0:
        return embedding  # Return original if norm is zero to avoid division by zero
    return (np_embedding / norm).tolist()

