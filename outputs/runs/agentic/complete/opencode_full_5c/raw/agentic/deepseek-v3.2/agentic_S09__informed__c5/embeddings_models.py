from typing import List, Optional
from dataclasses import dataclass


@dataclass
class EmbeddingRequest:
    """Request model for embedding generation."""

    text: str
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None


@dataclass
class EmbeddingResponse:
    """Response model for embedding generation."""

    embedding: List[float]
    model: str
    usage_tokens: Optional[int] = None


def normalize_text(text: str) -> str:
    """Normalize text for embedding generation."""
    if not text or not text.strip():
        return ""

    normalized = text.strip()

    if len(normalized) > 8192:
        normalized = normalized[:8192]

    return normalized


def parse_embedding_response(response_data) -> EmbeddingResponse:
    """Parse embedding response from API."""
    return EmbeddingResponse(
        embedding=response_data.embedding,
        model=response_data.model,
        usage_tokens=getattr(response_data, "usage", None),
    )
