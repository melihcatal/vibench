from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import numpy as np


@dataclass
class EmbeddingRequest:
    """Request model for embedding operations."""

    text: str
    model: str = "text-embedding-3-small"
    user: Optional[str] = None

    def to_api_format(self) -> Dict[str, Any]:
        """Convert to API request format."""
        request = {"input": self.text, "model": self.model, "encoding_format": "float"}
        if self.user:
            request["user"] = self.user
        return request


@dataclass
class BatchEmbeddingRequest:
    """Request model for batch embedding operations."""

    texts: List[str]
    model: str = "text-embedding-3-small"
    user: Optional[str] = None

    def to_api_format(self) -> Dict[str, Any]:
        """Convert to API request format."""
        request = {"input": self.texts, "model": self.model, "encoding_format": "float"}
        if self.user:
            request["user"] = self.user
        return request


@dataclass
class EmbeddingResponse:
    """Response model for embedding operations."""

    embedding: List[float]
    model: str
    usage: Dict[str, int]

    @classmethod
    def from_api_response(cls, api_response: Dict[str, Any]) -> "EmbeddingResponse":
        """Create from API response."""
        return cls(
            embedding=api_response["embedding"],
            model=api_response["model"],
            usage=api_response.get("usage", {"prompt_tokens": 0, "total_tokens": 0}),
        )


@dataclass
class BatchEmbeddingResponse:
    """Response model for batch embedding operations."""

    embeddings: List[List[float]]
    model: str
    usage: Dict[str, int]

    @classmethod
    def from_api_response(
        cls, api_response: Dict[str, Any]
    ) -> "BatchEmbeddingResponse":
        """Create from API response."""
        return cls(
            embeddings=[item["embedding"] for item in api_response["data"]],
            model=api_response["model"],
            usage=api_response.get("usage", {"prompt_tokens": 0, "total_tokens": 0}),
        )


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalize embedding vector to unit length."""
    vec = np.array(embedding)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return embedding
    normalized = vec / norm
    return normalized.tolist()


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Compute cosine similarity between two embeddings."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))
