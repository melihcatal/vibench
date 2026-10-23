"""
Local helper: Define request, response, and normalization helpers for Direct Embeddings API.
Provider: OpenAI Embeddings (openai SDK)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EmbeddingRequest:
    """Request payload wrapper for embedding calls."""
    text: str
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None
    encoding_format: str = "float"

    def to_openai_kwargs(self) -> Dict[str, Any]:
        """Convert to OpenAI client kwargs."""
        kwargs: Dict[str, Any] = {
            "input": self.text,
            "model": self.model,
            "encoding_format": self.encoding_format,
        }
        if self.dimensions is not None:
            kwargs["dimensions"] = self.dimensions
        return kwargs


@dataclass
class EmbeddingResponse:
    """Normalized response holding the embedding vector and metadata."""
    embedding: List[float] = field(default_factory=list)
    model: str = ""
    usage_tokens: int = 0
    index: int = 0


def normalize_embedding_vector(vector: List[float]) -> List[float]:
    """L2-normalize an embedding vector."""
    norm = math.sqrt(sum(x * x for x in vector))
    if norm == 0:
        return vector
    return [x / norm for x in vector]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(a) != len(b):
        raise ValueError("Vectors must have the same dimensionality")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def parse_openai_embedding_response(
    raw_response: Any,
    index: int = 0,
) -> EmbeddingResponse:
    """Parse a raw OpenAI embeddings response into an EmbeddingResponse."""
    data = raw_response.data[index]
    return EmbeddingResponse(
        embedding=list(data.embedding),
        model=raw_response.model,
        usage_tokens=raw_response.usage.total_tokens,
        index=index,
    )
