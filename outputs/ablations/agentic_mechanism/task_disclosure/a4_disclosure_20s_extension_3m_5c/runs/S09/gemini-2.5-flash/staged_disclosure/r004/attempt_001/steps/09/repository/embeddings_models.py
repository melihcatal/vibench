
from typing import List, Dict, Any

class DirectEmbeddingsRequest:
    """
    Represents a request to the Direct Embeddings API.
    """
    def __init__(self, texts: List[str], model: str = "text-embedding-ada-002"):
        self.texts = texts
        self.model = model

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input": self.texts,
            "model": self.model
        }

class DirectEmbeddingsResponse:
    """
    Represents a response from the Direct Embeddings API.
    """
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.embeddings = [item["embedding"] for item in data.get("data", [])]
        self.model = data.get("model")
        self.usage = data.get("usage")

    def get_embeddings(self) -> List[List[float]]:
        return self.embeddings

def normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    """
    Normalizes a list of embeddings. (Placeholder for actual normalization logic)
    """
    # In a real-world scenario, you would implement actual normalization here,
    # e.g., L2 normalization.
    return embeddings
