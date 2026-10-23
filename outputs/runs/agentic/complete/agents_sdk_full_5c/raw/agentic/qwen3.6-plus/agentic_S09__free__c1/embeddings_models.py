"""Local request, response, and normalization helpers for OpenAI Direct Embeddings API."""

from typing import List, Optional, Any, Union
from dataclasses import dataclass, field
import numpy as np


@dataclass
class EmbeddingRequest:
    """Request payload for OpenAI embeddings API.

    See: https://platform.openai.com/docs/api-reference/embeddings/create
    """
    input: Union[str, List[str]]
    model: str = "text-embedding-3-small"
    encoding_format: str = "float"
    dimensions: Optional[int] = None
    user: Optional[str] = None

    def to_dict(self) -> dict:
        payload = {
            "input": self.input,
            "model": self.model,
            "encoding_format": self.encoding_format,
        }
        if self.dimensions is not None:
            payload["dimensions"] = self.dimensions
        if self.user is not None:
            payload["user"] = self.user
        return payload


@dataclass
class EmbeddingUsage:
    """Token usage information from OpenAI API response."""
    prompt_tokens: int
    total_tokens: int


@dataclass
class EmbeddingResponse:
    """Normalized response from OpenAI embeddings API."""
    vector: List[float]
    model: str
    usage: Any = None
    raw_response: Any = None

    @property
    def dimension(self) -> int:
        return len(self.vector)

    def to_numpy(self) -> np.ndarray:
        return np.array(self.vector, dtype=np.float32)


@dataclass
class BatchEmbeddingResponse:
    """Response for batch embedding operations."""
    vectors: List[List[float]]
    models: List[str]
    total_tokens: int
    input_count: int

    def to_numpy_array(self) -> np.ndarray:
        return np.array(self.vectors, dtype=np.float32)

    @property
    def dimension(self) -> int:
        return len(self.vectors[0]) if self.vectors else 0


def normalize_vector(vector: Union[List[float], np.ndarray]) -> List[float]:
    """L2-normalize an embedding vector.

    OpenAI embeddings are already partially normalized, but explicit
    L2 normalization ensures consistent cosine similarity computation.

    Args:
        vector: Raw embedding vector from OpenAI API.

    Returns:
        L2-normalized vector as a list of floats.
    """
    if isinstance(vector, list):
        vec = np.array(vector, dtype=np.float64)
    else:
        vec = vector.astype(np.float64)

    norm = np.linalg.norm(vec)
    if norm == 0:
        return vector if isinstance(vector, list) else vector.tolist()

    normalized = vec / norm
    return normalized.tolist()


def truncate_to_dimension(
    vector: Union[List[float], np.ndarray],
    target_dimension: int,
) -> List[float]:
    """Truncate an embedding vector to a specific dimension.

    Useful when using OpenAI's text-embedding-3-small or text-embedding-3-large
    models with reduced dimensions for storage efficiency.

    Args:
        vector: Full embedding vector.
        target_dimension: Desired output dimension.

    Returns:
        Truncated vector as a list of floats.
    """
    if isinstance(vector, list):
        vec = np.array(vector, dtype=np.float32)
    else:
        vec = vector.astype(np.float32)

    truncated = vec[:target_dimension]
    return normalize_vector(truncated)


def parse_openai_response(raw_response: Any) -> EmbeddingResponse:
    """Parse a raw OpenAI API response into our normalized EmbeddingResponse."""
    data = raw_response.data[0]
    usage = EmbeddingUsage(
        prompt_tokens=raw_response.usage.prompt_tokens,
        total_tokens=raw_response.usage.total_tokens,
    )
    return EmbeddingResponse(
        vector=data.embedding,
        model=raw_response.model,
        usage=usage,
        raw_response=raw_response,
    )


def merge_vectors(
    vectors: List[Union[List[float], np.ndarray]],
    method: str = "mean",
) -> List[float]:
    """Merge multiple embedding vectors into a single vector.

    Args:
        vectors: List of vectors to merge.
        method: Merging strategy ('mean', 'max', 'sum').

    Returns:
        Merged and normalized vector.
    """
    np_vectors = [
        np.array(v, dtype=np.float32) if isinstance(v, list) else v.astype(np.float32)
        for v in vectors
    ]

    stacked = np.stack(np_vectors)

    if method == "mean":
        merged = np.mean(stacked, axis=0)
    elif method == "max":
        merged = np.max(stacked, axis=0)
    elif method == "sum":
        merged = np.sum(stacked, axis=0)
    else:
        raise ValueError(f"Unknown merge method: {method}")

    return normalize_vector(merged)
