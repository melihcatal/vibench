from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class EmbeddingRequest:
    """Data class for embedding request parameters."""

    text: str
    model: str = "text-embedding-3-small"
    encoding_format: str = "float"

    def to_openai_dict(self) -> Dict[str, Any]:
        """Convert to OpenAI API request format."""
        return {
            "model": self.model,
            "input": self.text,
            "encoding_format": self.encoding_format,
        }


@dataclass
class BatchEmbeddingRequest:
    """Data class for batch embedding request parameters."""

    texts: List[str]
    model: str = "text-embedding-3-small"
    encoding_format: str = "float"

    def to_openai_dict(self) -> Dict[str, Any]:
        """Convert to OpenAI API request format."""
        return {
            "model": self.model,
            "input": self.texts,
            "encoding_format": self.encoding_format,
        }


@dataclass
class EmbeddingResponse:
    """Data class for embedding response."""

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
class BatchEmbeddingResponse:
    """Data class for batch embedding response."""

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
    """Normalize an embedding vector to unit length."""
    vec = np.array(embedding)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return embedding
    normalized = vec / norm
    return normalized.tolist()


def validate_embedding_dimension(
    embedding: List[float], expected_dim: Optional[int] = None
) -> bool:
    """Validate embedding dimension matches expected size."""
    if expected_dim is None:
        return True
    return len(embedding) == expected_dim


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
