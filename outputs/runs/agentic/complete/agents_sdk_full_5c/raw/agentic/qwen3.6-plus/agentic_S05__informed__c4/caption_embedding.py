"""Embed caption chunks for semantic meeting search using OpenAI Embeddings API."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Sequence

import openai

from speech_models import FinalTranscript


OPENAI_API_ENV = "OPENAI_API_KEY"

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_DIMENSIONS = 1536


@dataclass
class CaptionEmbedding:
    """Represents an embedded caption chunk with its metadata."""
    text: str
    embedding: list[float]
    model: str
    dimensions: int
    index: int
    timestamp_offset: float = 0.0
    raw_response: Any | None = None


@dataclass
class EmbeddingBatch:
    """A batch of caption embeddings for indexing."""
    embeddings: list[CaptionEmbedding] = field(default_factory=list)
    total_tokens_used: int = 0
    model: str = DEFAULT_EMBEDDING_MODEL


def _get_openai_client() -> openai.OpenAI:
    """Create an OpenAI client using the API key from environment."""
    api_key = os.environ.get(OPENAI_API_ENV)
    if not api_key:
        raise EnvironmentError(
            f"Environment variable {OPENAI_API_ENV} is not set. "
            "Configure your OpenAI API key."
        )
    return openai.OpenAI(api_key=api_key)


def embed_caption_text(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int | None = None,
    index: int = 0,
) -> CaptionEmbedding:
    """
    Embed a single caption text using the OpenAI embeddings API.

    Parameters
    ----------
    text : str
        The caption text to embed.
    model : str
        OpenAI embedding model (e.g. text-embedding-3-small, text-embedding-3-large).
    dimensions : int | None
        Optional dimensions to truncate the embedding.
    index : int
        Position index for tracking order.
    """
    client = _get_openai_client()

    kwargs: dict[str, Any] = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    embedding_data = response.data[0]
    resolved_dimensions = dimensions or len(embedding_data.embedding)

    return CaptionEmbedding(
        text=text,
        embedding=embedding_data.embedding,
        model=model,
        dimensions=resolved_dimensions,
        index=index,
        raw_response=response,
    )


def embed_caption_batch(
    texts: Sequence[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int | None = None,
    start_index: int = 0,
) -> EmbeddingBatch:
    """
    Embed a batch of caption texts using the OpenAI embeddings API.

    Parameters
    ----------
    texts : Sequence[str]
        List of caption texts to embed.
    model : str
        OpenAI embedding model identifier.
    dimensions : int | None
        Optional dimensions for the embedding output.
    start_index : int
        Starting index for the embeddings.
    """
    client = _get_openai_client()

    kwargs: dict[str, Any] = {
        "input": texts,
        "model": model,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    embeddings: list[CaptionEmbedding] = []
    for i, data in enumerate(response.data):
        resolved_dimensions = dimensions or len(data.embedding)
        embeddings.append(
            CaptionEmbedding(
                text=texts[i],
                embedding=data.embedding,
                model=model,
                dimensions=resolved_dimensions,
                index=start_index + i,
            )
        )

    usage = response.usage.total_tokens if response.usage else 0
    return EmbeddingBatch(
        embeddings=embeddings,
        total_tokens_used=usage,
        model=model,
    )


async def stream_embed_captions(
    captions: AsyncIterator[FinalTranscript],
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int | None = None,
    batch_size: int = 5,
) -> AsyncIterator[EmbeddingBatch]:
    """
    Continuously embed incoming caption transcripts for semantic search.

    Buffers captions up to batch_size and emits EmbeddingBatch results
    using the OpenAI embeddings API.

    Parameters
    ----------
    captions : AsyncIterator[FinalTranscript]
        Async iterator of final transcript segments.
    model : str
        OpenAI embedding model identifier.
    dimensions : int | None
        Optional output dimensions.
    batch_size : int
        Number of captions to accumulate before embedding.
    """
    buffer: list[str] = []
    current_index = 0

    async for caption in captions:
        if caption.text and caption.text.strip():
            buffer.append(caption.text.strip())

        if len(buffer) >= batch_size:
            batch = embed_caption_batch(
                texts=buffer,
                model=model,
                dimensions=dimensions,
                start_index=current_index,
            )
            current_index += len(buffer)
            buffer.clear()
            yield batch

    if buffer:
        batch = embed_caption_batch(
            texts=buffer,
            model=model,
            dimensions=dimensions,
            start_index=current_index,
        )
        yield batch


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def search_similar_captions(
    query_embedding: list[float],
    caption_embeddings: list[CaptionEmbedding],
    top_k: int = 5,
) -> list[tuple[CaptionEmbedding, float]]:
    """
    Find the most similar caption embeddings to a query embedding.

    Returns a list of (CaptionEmbedding, similarity_score) tuples sorted by score.
    """
    scored: list[tuple[CaptionEmbedding, float]] = []
    for ce in caption_embeddings:
        score = cosine_similarity(query_embedding, ce.embedding)
        scored.append((ce, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
