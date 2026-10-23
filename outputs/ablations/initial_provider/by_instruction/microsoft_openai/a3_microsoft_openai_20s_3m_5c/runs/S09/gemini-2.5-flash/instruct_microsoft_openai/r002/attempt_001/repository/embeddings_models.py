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
        return [d["embedding"] for d in self.data]

class CombinedEmbeddingResult:
    def __init__(self, text: str, embedding: List[float]):
        self.text = text
        self.embedding = embedding
