from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class EmbeddingRequest:
    """Request model for embedding generation."""

    text: str
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None

    def to_openai_dict(self) -> Dict[str, Any]:
        """Convert to OpenAI API request format."""
        request = {"input": self.text, "model": self.model, "encoding_format": "float"}
        if self.dimensions:
            request["dimensions"] = self.dimensions
        return request


@dataclass
class EmbeddingResponse:
    """Response model for embedding generation."""

    embedding: List[float]
    model: str
    usage_tokens: int

    @classmethod
    def from_openai_response(cls, openai_response: Any) -> "EmbeddingResponse":
        """Create from OpenAI API response."""
        return cls(
            embedding=openai_response.data[0].embedding,
            model=openai_response.model,
            usage_tokens=openai_response.usage.total_tokens,
        )


@dataclass
class BatchEmbeddingRequest:
    """Request model for batch embedding generation."""

    texts: List[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None

    def to_openai_dict(self) -> Dict[str, Any]:
        """Convert to OpenAI API request format."""
        request = {"input": self.texts, "model": self.model, "encoding_format": "float"}
        if self.dimensions:
            request["dimensions"] = self.dimensions
        return request


@dataclass
class BatchEmbeddingResponse:
    """Response model for batch embedding generation."""

    embeddings: List[List[float]]
    model: str
    usage_tokens: int

    @classmethod
    def from_openai_response(cls, openai_response: Any) -> "BatchEmbeddingResponse":
        """Create from OpenAI API response."""
        return cls(
            embeddings=[item.embedding for item in openai_response.data],
            model=openai_response.model,
            usage_tokens=openai_response.usage.total_tokens,
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
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
