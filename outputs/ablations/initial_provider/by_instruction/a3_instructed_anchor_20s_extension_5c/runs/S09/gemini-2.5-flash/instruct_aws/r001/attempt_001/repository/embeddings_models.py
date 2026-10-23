import json
from typing import List, Dict, Any

class EmbeddingRequest:
    """
    Represents a request for embedding generation.
    """
    def __init__(self, text: str):
        self.inputText = text

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

class EmbeddingResponse:
    """
    Represents a response from the embedding API.
    """
    def __init__(self, response_body: Dict[str, Any]):
        self.embedding = response_body.get("embedding", [])

    def get_embedding(self) -> List[float]:
        return self.embedding

def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    Placeholder for any embedding normalization logic.
    For AWS Titan, the embeddings are typically ready to use directly.
    """\n    return embedding
