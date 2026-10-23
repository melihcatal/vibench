"""
Local helper: Define request, response, and normalization helpers for Direct Embeddings API.
Provider: OpenAI Embeddings API
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class EmbeddingRequest:
    """Normalized request payload for a single or batch embedding call."""
    model: str
    input_texts: List[str]
    dimensions: Optional[int] = None
    encoding_format: str = "float"


@dataclass
class EmbeddingResult:
    """Single embedding result returned by the provider."""
    text: str
    vector: List[float]
    index: int = 0
    model: str = ""


@dataclass
class EmbeddingBatchResponse:
    """Aggregated response for a batch embedding call."""
    results: List[EmbeddingResult] = field(default_factory=list)
    model: str = ""
    total_tokens: int = 0


def normalize_vector(vector: List[float]) -> List[float]:
    """L2-normalize an embedding vector."""
    magnitude = math.sqrt(sum(v * v for v in vector))
    if magnitude == 0:
        return vector
    return [v / magnitude for v in vector]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensionality.")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def build_embedding_request(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> EmbeddingRequest:
    """Construct a normalized embedding request."""
    return EmbeddingRequest(
        model=model,
        input_texts=texts,
        dimensions=dimensions,
    )


def parse_openai_response(raw_response) -> EmbeddingBatchResponse:
    """Parse an OpenAI API response into an EmbeddingBatchResponse."""
    results = []
    for item in raw_response.data:
        results.append(
            EmbeddingResult(
                text=item.get("text", ""),
                vector=item.embedding,
                index=item.index,
                model=raw_response.model,
            )
        )
    usage = getattr(raw_response, "usage", None)
    total_tokens = usage.total_tokens if usage else 0
    return EmbeddingBatchResponse(
        results=results,
        model=raw_response.model,
        total_tokens=total_tokens,
    )
