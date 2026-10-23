import numpy as np
from typing import List, Dict, Any

class EmbeddingRequest:
    """Represents a request for embeddings."""
    def __init__(self, texts: List[str], model: str = "models/embedding-001", task_type: str = "RETRIEVAL_DOCUMENT"):
        self.texts = texts
        self.model = model
        self.task_type = task_type

    def to_gemini_payload(self) -> Dict[str, Any]:
        """Converts the request to a payload suitable for the Google Gemini Embeddings API."""
        return {
            "model": self.model,
            "content": self.texts,
            "task_type": task_type
        }

class EmbeddingResponse:
    """Represents a response containing embedding vectors."""
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings

    @classmethod
    def from_gemini_response(cls, api_response: Dict[str, Any]):
        """Creates an EmbeddingResponse from a Google Gemini Embeddings API response."""
        return cls(embeddings=api_response.get("embedding", []))

def calculate_cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculates the cosine similarity between two embedding vectors.
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0

    return dot_product / (norm_vec1 * norm_vec2)

if __name__ == '__main__':
    # Example usage
    req = EmbeddingRequest(texts=["hello", "world"])
    print(f"Gemini payload example: {req.to_gemini_payload()}")

    # Simulate a Gemini API response
    dummy_gemini_response = {
        "embedding": [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6]
        ]
    }
    resp = EmbeddingResponse.from_gemini_response(dummy_gemini_response)
    print(f"Parsed embeddings: {resp.embeddings}")

    # Example cosine similarity
    emb1 = [0.1, 0.2, 0.3]
    emb2 = [0.15, 0.25, 0.35]
    similarity = calculate_cosine_similarity(emb1, emb2)
    print(f"Cosine similarity of dummy embeddings: {similarity:.4f}")
