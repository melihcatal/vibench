from typing import List, Dict, Any

EmbeddingVector = List[float]

class EmbeddingRequest:
    def __init__(self, texts: List[str], model: str):
        self.texts = texts
        self.model = model

class EmbeddingResponse:
    def __init__(self, data: List[Dict[str, Any]], model: str):
        self.data = data
        self.model = model