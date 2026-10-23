import numpy as np
from typing import List


def normalize_to_numpy(embeddings: List[List[float]]) -> np.ndarray:
    return np.array(embeddings)


class EmbeddingRequest:
    def __init__(self, texts: List[str], model: str = "embed-english-v3.0"):
        self.texts = texts
        self.model = model


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings
