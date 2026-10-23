
"""
Local request, response, and normalization helpers for Direct Embeddings API.
"""

from typing import List, Dict, Any

class EmbeddingRequest:
    """
    Represents a local request for the Direct Embeddings API.
    """
    def __init__(self, texts: List[str], model_id: str = "default_model"):
        self.texts = texts
        self.model_id = model_id

    def to_api_format(self) -> Dict[str, Any]:
        """Converts the local request to the format expected by the Direct Embeddings API."""
        return {
            "instances": [{"text": text} for text in self.texts],
            "model_id": self.model_id
        }

class EmbeddingResponse:
    """
    Represents a local response from the Direct Embeddings API.
    """
    def __init__(self, predictions: List[Dict[str, Any]]):
        self.predictions = predictions

    @classmethod
    def from_api_format(cls, api_response: Dict[str, Any]):
        """Creates a local response object from the Direct Embeddings API's response format."""
        return cls(api_response.get("predictions", []))

    def get_embeddings(self) -> List[List[float]]:
        """Extracts and returns the embeddings from the response."""
        embeddings = []
        for prediction in self.predictions:
            if "embedding" in prediction:
                embeddings.append(prediction["embedding"])
        return embeddings

def normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    """
    Normalizes a list of embeddings.
    (Placeholder for actual normalization logic, e.g., L2 normalization)
    """
    normalized_embeddings = []
    for embedding in embeddings:
        # Example: L2 normalization
        magnitude = sum(x**2 for x in embedding)**0.5
        if magnitude == 0:
            normalized_embeddings.append(embedding)  # Avoid division by zero
        else:
            normalized_embeddings.append([x / magnitude for x in embedding])
    return normalized_embeddings

