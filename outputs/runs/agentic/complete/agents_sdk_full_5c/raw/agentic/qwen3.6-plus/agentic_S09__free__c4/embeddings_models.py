"""
Define local request, response, and normalization helpers for Direct Embeddings API.
Provider: OpenAI (api.openai.com) with text-embedding-3-small and text-embedding-3-large models.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import math


@dataclass
class EmbeddingRequest:
    """Normalized request model for OpenAI embedding calls."""
    text: str
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    encoding_format: str = "float"

    def to_openai_payload(self) -> Dict[str, Any]:
        """Convert to OpenAI API payload format."""
        payload: Dict[str, Any] = {
            "model": self.model,
            "input": self.text,
            "encoding_format": self.encoding_format,
        }
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass
class BatchEmbeddingRequest:
    """Normalized request model for batch OpenAI embedding calls."""
    texts: List[str]
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    encoding_format: str = "float"

    def to_openai_payload(self) -> Dict[str, Any]:
        """Convert to OpenAI API payload format."""
        payload: Dict[str, Any] = {
            "model": self.model,
            "input": self.texts,
            "encoding_format": self.encoding_format,
        }
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        return payload


@dataclass
class EmbeddingResponse:
    """Normalized response model from OpenAI embedding API."""
    embedding: List[float]
    model: str
    usage_tokens: int
    index: int = 0

    @classmethod
    def from_openai_response(cls, response_data: Any, index: int = 0) -> "EmbeddingResponse":
        """Parse from OpenAI API response."""
        if hasattr(response_data, "data"):
            item = response_data.data[index]
            usage = response_data.usage.total_tokens if response_data.usage else 0
            return cls(
                embedding=item.embedding,
                model=response_data.model,
                usage_tokens=usage,
                index=index,
            )
        if isinstance(response_data, dict):
            item = response_data["data"][index]
            usage = response_data.get("usage", {}).get("total_tokens", 0)
            return cls(
                embedding=item["embedding"],
                model=response_data["model"],
                usage_tokens=usage,
                index=index,
            )
        raise ValueError("Invalid OpenAI response format")


@dataclass
class BatchEmbeddingResponse:
    """Normalized response model for batch OpenAI embedding calls."""
    embeddings: List[List[float]]
    models: List[str]
    total_usage_tokens: int

    @classmethod
    def from_openai_response(cls, response_data: Any) -> "BatchEmbeddingResponse":
        """Parse from OpenAI API batch response."""
        if hasattr(response_data, "data"):
            embeddings = [item.embedding for item in response_data.data]
            models = [item.model if hasattr(item, "model") else response_data.model
                      for item in response_data.data]
            usage = response_data.usage.total_tokens if response_data.usage else 0
            return cls(
                embeddings=embeddings,
                models=models,
                total_usage_tokens=usage,
            )
        if isinstance(response_data, dict):
            embeddings = [item["embedding"] for item in response_data["data"]]
            models = [item.get("model", response_data["model"])
                      for item in response_data["data"]]
            usage = response_data.get("usage", {}).get("total_tokens", 0)
            return cls(
                embeddings=embeddings,
                models=models,
                total_usage_tokens=usage,
            )
        raise ValueError("Invalid OpenAI response format")


def normalize_vector(vec: List[float]) -> List[float]:
    """L2-normalize an embedding vector."""
    magnitude = math.sqrt(sum(x * x for x in vec))
    if magnitude == 0:
        return vec
    return [x / magnitude for x in vec]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensionality")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(x * x for x in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def truncate_embedding(vec: List[float], target_dim: int) -> List[float]:
    """Truncate embedding to target dimensions (OpenAI supports this natively)."""
    return vec[:target_dim]


def validate_embedding_response(response_data: Any) -> bool:
    """Validate that an OpenAI response contains expected fields."""
    if hasattr(response_data, "data"):
        return (
            hasattr(response_data, "data")
            and len(response_data.data) > 0
            and hasattr(response_data.data[0], "embedding")
        )
    if isinstance(response_data, dict):
        return (
            "data" in response_data
            and len(response_data["data"]) > 0
            and "embedding" in response_data["data"][0]
        )
    return False
