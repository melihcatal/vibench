"""
Embed caption chunks for semantic meeting search using OpenAI Embeddings API.

Converts live caption text into vector embeddings via OpenAI's text-embedding
service, enabling semantic search over meeting content.

Provider: OpenAI Embeddings API
SDK: openai
Auth: OPENAI_API_KEY
"""

from __future__ import annotations

import os
import time
from typing import AsyncGenerator, Optional

from openai import OpenAI

# OpenAI Embeddings provider constants
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSIONS = 1536


def _get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """
    Create an OpenAI client for embedding generation.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Configured OpenAI client instance.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable must be set or api_key provided."
        )
    return OpenAI(api_key=key)


def embed_caption_chunk(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> list[float]:
    """
    Embed a single caption chunk using OpenAI Embeddings API.

    Args:
        text: Caption text to embed.
        model: OpenAI embedding model (e.g., 'text-embedding-3-small',
               'text-embedding-3-large', 'text-embedding-ada-002').
        api_key: OpenAI API key.

    Returns:
        List of float values representing the embedding vector.
    """
    client = _get_openai_client(api_key)

    response = client.embeddings.create(
        model=model,
        input=text,
        dimensions=OPENAI_EMBEDDING_DIMENSIONS,
    )

    return response.data[0].embedding


async def embed_live_captions(
    caption_stream: AsyncGenerator[str, None],
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    metadata_extractor: Optional[callable] = None,
) -> AsyncGenerator[dict, None]:
    """
    Embed live caption chunks for semantic meeting search using OpenAI Embeddings API.

    Processes each caption text from the async stream, generates embeddings
    via the OpenAI text-embedding-3-small model, and yields embeddable
    records suitable for vector database storage and semantic search.

    Args:
        caption_stream: Async generator yielding caption text strings.
        model: OpenAI embedding model identifier.
        api_key: OpenAI API key.
        metadata_extractor: Optional callable to extract metadata from caption text.

    Yields:
        Dict with keys:
            - 'chunk_index': Sequential index of the processed chunk
            - 'text': Original caption text
            - 'embedding': Vector embedding (list of floats)
            - 'model': Embedding model used
            - 'dimensions': Embedding dimensionality
            - 'timestamp': Processing timestamp
            - 'metadata': Optional extracted metadata
    """
    client = _get_openai_client(api_key)
    chunk_index = 0

    async for caption in caption_stream:
        if not caption.strip():
            continue

        try:
            response = client.embeddings.create(
                model=model,
                input=caption,
                dimensions=OPENAI_EMBEDDING_DIMENSIONS,
            )

            embedding = response.data[0].embedding

            metadata = None
            if metadata_extractor:
                metadata = metadata_extractor(caption)

            yield {
                "chunk_index": chunk_index,
                "text": caption,
                "embedding": embedding,
                "model": model,
                "dimensions": len(embedding),
                "timestamp": time.time(),
                "metadata": metadata,
            }

            chunk_index += 1

        except Exception as e:
            yield {
                "chunk_index": chunk_index,
                "text": caption,
                "embedding": [],
                "model": model,
                "dimensions": 0,
                "timestamp": time.time(),
                "metadata": None,
                "error": str(e),
            }
            chunk_index += 1
