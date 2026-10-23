"""
Local request, response, and normalization helpers for Direct Embeddings API.

Provider: OpenAI Embeddings API
Provider SDK: openai
Provider Model: text-embedding-3-small / text-embedding-3-large
"""

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EmbeddingRequest:
    """Normalized request payload for embedding generation."""
    text: str = ""
    texts: list[str] = field(default_factory=list)
    model: str = "text-embedding-3-small"
    dimensions: int = 1536


@dataclass
class EmbeddingResponse:
    """Normalized response container for embedding results."""
    embedding: list[float] = field(default_factory=list)
    embeddings: list[list[float]] = field(default_factory=list)
    model: str = ""
    usage: dict[str, Any] = field(default_factory=dict)
    raw_response: Any = None


@dataclass
class SearchResult:
    """Container for a semantic search result."""
    document: str
    score: float
    index: int


def l2_normalize(vec: list[float]) -> list[float]:
    """L2-normalize a vector."""
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0:
        return vec
    return [x / norm for x in vec]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(a) != len(b):
        raise ValueError("Vectors must have the same dimensionality")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def normalize_request(texts: str | list[str], model: str, dimensions: int) -> EmbeddingRequest:
    """Build a normalized EmbeddingRequest from raw inputs."""
    if isinstance(texts, str):
        return EmbeddingRequest(text=texts, model=model, dimensions=dimensions)
    return EmbeddingRequest(texts=texts, model=model, dimensions=dimensions)


def build_search_results(documents: list[str], scores: list[float]) -> list[SearchResult]:
    """Build SearchResult list from documents and their scores."""
    results = []
    for i, (doc, score) in enumerate(zip(documents, scores)):
        results.append(SearchResult(document=doc, score=score, index=i))
    return sorted(results, key=lambda r: r.score, reverse=True)
