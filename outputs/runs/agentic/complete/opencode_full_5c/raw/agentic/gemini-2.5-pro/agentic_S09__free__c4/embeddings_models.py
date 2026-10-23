from typing import List, Union
import numpy as np


def normalize_embeddings(embeddings: List[List[float]]) -> np.ndarray:
    """
    Normalize embeddings to unit length.
    """
    embeddings_array = np.array(embeddings)
    norms = np.linalg.norm(embeddings_array, axis=1, keepdims=True)
    return embeddings_array / norms


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]], model: str):
        self.embeddings = embeddings
        self.model = model


class SearchEmbeddingResponse:
    def __init__(
        self,
        query_embedding: List[float],
        document_embeddings: List[List[float]],
        model: str,
    ):
        self.query_embedding = query_embedding
        self.document_embeddings = document_embeddings
        self.model = model
