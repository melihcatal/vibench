"""
embeddings_models.py - Define local request, response, and normalization helpers
for Direct Embeddings API.

Provider: OpenAI Embeddings API
SDK: openai
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EmbeddingRequest:
    """Normalized request payload for the OpenAI Embeddings API."""

    input: str | list[str]
    model: str = "text-embedding-3-small"
    dimensions: int | None = None
    encoding_format: str = "float"

    def to_openai_params(self) -> dict[str, Any]:
        """Convert to parameters suitable for OpenAI client.embeddings.create()."""
        params: dict[str, Any] = {
            "model": self.model,
            "input": self.input,
            "encoding_format": self.encoding_format,
        }
        if self.dimensions is not None:
            params["dimensions"] = self.dimensions
        return params


@dataclass
class EmbeddingVector:
    """A single embedding result with metadata."""

    index: int
    vector: list[float]
    model: str = ""
    usage_tokens: int = 0

    @property
    def magnitude(self) -> float:
        return math.sqrt(sum(v * v for v in self.vector))

    def normalized(self) -> list[float]:
        mag = self.magnitude
        if mag == 0.0:
            return list(self.vector)
        return [v / mag for v in self.vector]


@dataclass
class EmbeddingResponse:
    """Normalized response container for OpenAI embeddings results."""

    vectors: list[EmbeddingVector] = field(default_factory=list)
    model: str = ""
    total_tokens: int = 0

    def get_vector(self, index: int = 0) -> EmbeddingVector | None:
        for v in self.vectors:
            if v.index == index:
                return v
        return None if not self.vectors else self.vectors[0]

    def as_matrix(self) -> list[list[float]]:
        return [v.vector for v in sorted(self.vectors, key=lambda x: x.index)]


def parse_openai_embedding_response(response: Any) -> EmbeddingResponse:
    """Parse an OpenAI SDK response into an EmbeddingResponse."""
    result = EmbeddingResponse()

    if hasattr(response, "data"):
        for item in response.data:
            vec = EmbeddingVector(
                index=item.index,
                vector=item.embedding,
            )
            result.vectors.append(vec)

    if hasattr(response, "model"):
        result.model = response.model

    if hasattr(response, "usage"):
        result.total_tokens = response.usage.total_tokens if response.usage else 0
    elif isinstance(response, dict):
        result.model = response.get("model", "")
        usage = response.get("usage", {})
        result.total_tokens = usage.get("total_tokens", 0)
        for item in response.get("data", []):
            vec = EmbeddingVector(
                index=item.get("index", 0),
                vector=item.get("embedding", []),
            )
            result.vectors.append(vec)

    return result


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if len(a) != len(b):
        raise ValueError("Vectors must have the same dimensionality")

    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))

    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
