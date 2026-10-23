# [HELPER] embeddings_models.py
# Local request/response helpers for Direct Embeddings API

from typing import List, Dict, Any


class EmbedRequest:
    """Container for embedding request payload."""

    def __init__(self, texts: List[str]):
        self.texts = texts


class EmbedResponse:
    """Container for embedding response payload."""

    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data


def parse_embedding_response(raw: Dict[str, Any]) -> List[list[float]]:
    """Extract embedding vectors from raw API response."""
    return [item["embedding"] for item in raw.get("data", [])]
