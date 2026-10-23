"""
Define local request, response, and normalization helpers for Direct Embeddings API.
Provider: OpenAI embeddings (api.openai.com, model text-embedding-3-small).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EmbeddingRequest:
    """Request payload for a single or batch embedding call."""
    input_texts: list[str]
    model: str = "text-embedding-3-small"
    dimensions: int | None = None
    encoding_format: str = "float"

    def to_openai_kwargs(self) -> dict[str, Any]:
        """Convert to kwargs suitable for openai.embeddings.create()."""
        kwargs: dict[str, Any] = {
            "input": self.input_texts,
            "model": self.model,
            "encoding_format": self.encoding_format,
        }
        if self.dimensions is not None:
            kwargs["dimensions"] = self.dimensions
        return kwargs


@dataclass
class EmbeddingResult:
    """A single embedding vector with metadata."""
    text: str
    vector: list[float]
    index: int
    usage_tokens: int = 0


@dataclass
class EmbeddingResponse:
    """Aggregated response from a batch embedding call."""
    results: list[EmbeddingResult] = field(default_factory=list)
    total_tokens: int = 0
    model: str = ""

    @classmethod
    def from_openai_response(
        cls,
        raw_response: Any,
        texts: list[str],
    ) -> "EmbeddingResponse":
        """Parse an openai.types.CreateEmbeddingResponse into EmbeddingResponse."""
        results = []
        total_tokens = getattr(raw_response, "usage", None)
        total_tokens = total_tokens.total_tokens if total_tokens else 0

        for data_item in raw_response.data:
            idx = data_item.index
            results.append(
                EmbeddingResult(
                    text=texts[idx] if idx < len(texts) else "",
                    vector=list(data_item.embedding),
                    index=idx,
                )
            )

        return cls(
            results=sorted(results, key=lambda r: r.index),
            total_tokens=total_tokens,
            model=getattr(raw_response, "model", ""),
        )


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError(
            f"Vector dimension mismatch: {len(vec_a)} vs {len(vec_b)}"
        )

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def normalize_vector(vec: list[float]) -> list[float]:
    """L2-normalize an embedding vector."""
    magnitude = math.sqrt(sum(v * v for v in vec))
    if magnitude == 0.0:
        return vec[:]
    return [v / magnitude for v in vec]


def chunk_texts(texts: list[str], max_chunk_size: int = 200) -> list[list[str]]:
    """Split a list of texts into chunks for batch API calls (OpenAI limit)."""
    chunks = []
    for i in range(0, len(texts), max_chunk_size):
        chunks.append(texts[i : i + max_chunk_size])
    return chunks
