from typing import List, Dict


class EmbedRequest:
    """Container for embedding request payloads."""

    def __init__(self, text: str):
        self.text = text


class EmbedResponse:
    """Container for embedding response payloads."""

    def __init__(self, embedding: List[float]):
        self.embedding = embedding


def normalize_embedding(response: Dict) -> List[float]:
    """Normalize provider-specific embedding payload to a simple list."""
    # Example assumes response has key 'embedding' with list value
    return response.get("embedding", [])
