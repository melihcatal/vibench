from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class EmbeddingRequest:
    """Request model for embedding generation."""

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
    """Request model for batch embedding generation."""

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
    """Response model for embedding generation."""

    embedding: List[float]
    model: str
    usage: Optional[Dict[str, int]] = None

    @classmethod
    def from_openai_response(cls, openai_response: Any) -> "EmbeddingResponse":
        """Create from OpenAI API response."""
        return cls(
            embedding=openai_response.data[0].embedding,
            model=openai_response.model,
            usage={
                "prompt_tokens": openai_response.usage.prompt_tokens,
                "total_tokens": openai_response.usage.total_tokens,
            }
            if hasattr(openai_response, "usage")
            else None,
        )


@dataclass
class BatchEmbeddingResponse:
    """Response model for batch embedding generation."""

    embeddings: List[List[float]]
    model: str
    usage: Optional[Dict[str, int]] = None

    @classmethod
    def from_openai_response(cls, openai_response: Any) -> "BatchEmbeddingResponse":
        """Create from OpenAI API response."""
        return cls(
            embeddings=[item.embedding for item in openai_response.data],
            model=openai_response.model,
            usage={
                "prompt_tokens": openai_response.usage.prompt_tokens,
                "total_tokens": openai_response.usage.total_tokens,
            }
            if hasattr(openai_response, "usage")
            else None,
        )


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalize embedding vector to unit length."""
    vec = np.array(embedding)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()


def compute_cosine_similarity(
    embedding1: List[float], embedding2: List[float]
) -> float:
    """Compute cosine similarity between two embeddings."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    # Normalize vectors
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    cosine_similarity = np.dot(vec1, vec2) / (norm1 * norm2)
    return float(cosine_similarity)
