import os
from typing import List, Dict, Any


class EmbeddingRequest:
    def __init__(self, texts: List[str], model: str = "text-embedding-ada-002"):
        self.texts = texts
        self.model = model


class EmbeddingResponse:
    def __init__(self, data: List[Dict[str, Any]], model: str):
        self.data = data
        self.model = model

    def get_embeddings(self) -> List[List[float]]:
        return [item["embedding"] for item in self.data]


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Placeholder for any necessary normalization."""
    return embedding
