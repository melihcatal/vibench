from typing import List


class EmbeddingRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings


def normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    return [embedding / np.linalg.norm(embedding) for embedding in embeddings]
