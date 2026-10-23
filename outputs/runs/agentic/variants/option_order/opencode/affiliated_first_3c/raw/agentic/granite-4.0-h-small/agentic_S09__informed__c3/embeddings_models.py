import json
from typing import TypedDict, List

# Type definitions for request payloads


class EmbedRequest(TypedDict):
    """Payload for embedding a single or multiple texts."""

    text: str | List[str]


# Type definitions for response payloads


class EmbedResponse(TypedDict):
    """Response from the embeddings endpoint."""

    id: str
    embedding: List[float]


class BatchEmbedResponse(TypedDict):
    """Response for batch embeddings."""

    embeddings: List[EmbedResponse]


# Normalization helpers


def normalize_embedding_response(raw: dict) -> EmbedResponse:
    """Convert raw API dict to the canonical EmbedResponse type."""
    return EmbedResponse(id=raw.get("id", ""), embedding=raw.get("embedding", []))


def normalize_batch_response(raw: dict) -> BatchEmbedResponse:
    """Convert raw API dict to the canonical BatchEmbedResponse type."""
    return BatchEmbedResponse(
        embeddings=[
            normalize_embedding_response(item) for item in raw.get("embeddings", [])
        ]
    )
