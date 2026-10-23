from typing import List


class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]], query_embedding: List[float] = None, document_embeddings: List[List[float]] = None):
        self.embeddings = embeddings
        self.query_embedding = query_embedding
        self.document_embeddings = document_embeddings