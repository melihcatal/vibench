from typing import Any, Dict, List


class EmbeddingRequest:
    def __init__(self, text: str, model: str):
        self.text = text
        self.model = model

    def to_dict(self) -> Dict[str, Any]:
        return {
            'text': self.text,
            'model': self.model
        }


class EmbeddingResponse:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(embedding=data['embedding'])


def normalize_embedding(embedding: List[float]) -> List[float]:
    import numpy as np
    embedding_array = np.array(embedding)
    norm = np.linalg.norm(embedding_array)
    if norm == 0:
        return embedding
    return embedding_array / norm


def denormalize_embedding(normalized_embedding: List[float], original_norm: float) -> List[float]:
    import numpy as np
    normalized_array = np.array(normalized_embedding)
    return (normalized_array * original_norm).tolist()
