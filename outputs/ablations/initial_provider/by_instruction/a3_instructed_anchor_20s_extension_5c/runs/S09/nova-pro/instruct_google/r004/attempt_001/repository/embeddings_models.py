from typing import List

class EmbeddingRequest:
    def __init__(self, contents: List[str], model: str):
        self.contents = contents
        self.model = model

class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings

def normalize_embedding(embedding):
    return [float(value) for value in embedding]