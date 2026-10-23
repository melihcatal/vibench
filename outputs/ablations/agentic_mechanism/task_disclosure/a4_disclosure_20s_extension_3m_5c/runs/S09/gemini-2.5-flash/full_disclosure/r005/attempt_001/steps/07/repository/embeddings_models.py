import numpy as np

class EmbeddingRequest:
    def __init__(self, text_content: str, model_id: str):
        self.text_content = text_content
        self.model_id = model_id

    def to_dict(self):
        return {
            "text_content": self.text_content,
            "model_id": self.model_id
        }

class EmbeddingResponse:
    def __init__(self, embedding: list[float]):
        self.embedding = embedding

    @classmethod
    def from_dict(cls, data: dict):
        return cls(embedding=data["embedding"])

def normalize_embedding(embedding: list[float]) -> list[float]:
    """Normalizes an embedding vector to a unit vector."""
    if not embedding:
        return []
    vec = np.array(embedding)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return embedding
    return (vec / norm).tolist()
