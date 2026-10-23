from typing import List, Dict, Any


class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalizes an embedding vector."""
    magnitude = sum(x**2 for x in embedding) ** 0.5
    if magnitude == 0:
        return [0.0] * len(embedding)
    return [x / magnitude for x in embedding]
