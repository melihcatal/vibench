"""
Embed caption chunks for semantic meeting search using OpenAI Embeddings API.

This module converts live speech-to-text caption chunks into dense vector
embeddings using the OpenAI Embeddings API (api.openai.com) with the
text-embedding-3-small model. Generated embeddings enable semantic similarity
search across meeting transcripts for post-meeting analysis and retrieval.
"""

import asyncio
import json
import logging
import os
from typing import AsyncIterator, List, Optional

import numpy as np
import httpx

logger = logging.getLogger(__name__)

OPENAI_API_ENDPOINT = "https://api.openai.com/v1"
OPENAI_EMBEDDINGS_URL = f"{OPENAI_API_ENDPOINT}/embeddings"
OPENAI_EMBEDDING_MODEL_ID = "text-embedding-3-small"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


class CaptionEmbedding:
    """A caption chunk with its associated embedding vector and metadata."""

    def __init__(
        self,
        text: str,
        embedding: List[float],
        index: int = 0,
        timestamp_ms: float = 0.0,
        is_final: bool = False,
        model: str = OPENAI_EMBEDDING_MODEL_ID,
    ):
        self.text = text
        self.embedding = embedding
        self.index = index
        self.timestamp_ms = timestamp_ms
        self.is_final = is_final
        self.model = model

    @property
    def vector(self) -> np.ndarray:
        """Return the embedding as a numpy array."""
        return np.array(self.embedding, dtype=np.float32)

    def similarity(self, other: "CaptionEmbedding") -> float:
        """Compute cosine similarity with another embedding."""
        a = self.vector
        b = other.vector
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def to_dict(self) -> dict:
        """Serialize to a dictionary."""
        return {
            "text": self.text,
            "embedding": self.embedding,
            "index": self.index,
            "timestamp_ms": self.timestamp_ms,
            "is_final": self.is_final,
            "model": self.model,
        }


class CaptionEmbeddingStore:
    """
    Store and search caption embeddings for semantic meeting search.

    Maintains a collection of CaptionEmbedding objects generated from
    OpenAI's text-embedding-3-small model and supports similarity search.
    """

    def __init__(self):
        self._embeddings: List[CaptionEmbedding] = []
        self._vectors: Optional[np.ndarray] = None

    def add(self, embedding: CaptionEmbedding) -> None:
        """Add a caption embedding to the store."""
        self._embeddings.append(embedding)
        self._vectors = None

    def search(
        self,
        query_embedding: CaptionEmbedding,
        top_k: int = 5,
        min_similarity: float = 0.0,
    ) -> List[dict]:
        """
        Find the most similar caption embeddings to a query.

        Args:
            query_embedding: Query embedding to search against.
            top_k: Number of results to return.
            min_similarity: Minimum cosine similarity threshold.

        Returns:
            List of dicts with embedding data and similarity scores.
        """
        if not self._embeddings:
            return []

        query_vec = query_embedding.vector
        results = []

        for emb in self._embeddings:
            sim = query_embedding.similarity(emb)
            if sim >= min_similarity:
                results.append({
                    "text": emb.text,
                    "similarity": sim,
                    "index": emb.index,
                    "timestamp_ms": emb.timestamp_ms,
                    "is_final": emb.is_final,
                })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    @property
    def count(self) -> int:
        """Return the number of stored embeddings."""
        return len(self._embeddings)


class CaptionEmbedder:
    """
    Generate embeddings for caption chunks using the OpenAI Embeddings API.

    Sends text to api.openai.com using the text-embedding-3-small model
    and receives dense vector embeddings suitable for semantic search.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = OPENAI_EMBEDDING_MODEL_ID,
        dimensions: Optional[int] = None,
    ):
        """
        Initialize the caption embedder.

        Args:
            api_key: OpenAI API key for authentication.
            model: OpenAI embedding model identifier (e.g., 'text-embedding-3-small').
            dimensions: Optional output dimensionality for the embedding.
        """
        self._api_key = api_key or os.environ.get(OPENAI_API_KEY_ENV, "")
        self._model = model
        self._dimensions = dimensions
        self._total_embedded: int = 0

        if not self._api_key:
            logger.warning(
                "%s not set; OpenAI Embedding API calls to %s will fail",
                OPENAI_API_KEY_ENV,
                OPENAI_API_ENDPOINT,
            )

        logger.info(
            "CaptionEmbedder initialized with model=%s via %s",
            model,
            OPENAI_API_ENDPOINT,
        )

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding vector for a text string using OpenAI.

        Sends the text to api.openai.com via the embeddings endpoint
        with the text-embedding-3-small model.

        Args:
            text: Text to embed.

        Returns:
            List of floats representing the dense embedding vector.
        """
        if not text or not text.strip():
            return []

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        payload: dict = {
            "model": self._model,
            "input": [text.strip()],
        }
        if self._dimensions is not None:
            payload["dimensions"] = self._dimensions

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENAI_EMBEDDINGS_URL,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

        data = result.get("data", [])
        if not data:
            logger.error("No embedding data returned from %s", OPENAI_API_ENDPOINT)
            return []

        embedding = data[0].get("embedding", [])
        self._total_embedded += 1

        logger.debug(
            "Generated embedding #%d via OpenAI %s (model=%s, dim=%d)",
            self._total_embedded,
            OPENAI_API_ENDPOINT,
            self._model,
            len(embedding),
        )

        return embedding

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple text strings in a single API call.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of embedding vectors (list of list of floats).
        """
        filtered = [t.strip() for t in texts if t and t.strip()]
        if not filtered:
            return []

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        payload: dict = {
            "model": self._model,
            "input": filtered,
        }
        if self._dimensions is not None:
            payload["dimensions"] = self._dimensions

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OPENAI_EMBEDDINGS_URL,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

        embeddings = []
        for item in result.get("data", []):
            embeddings.append(item.get("embedding", []))

        self._total_embedded += len(embeddings)
        return embeddings


async def stream_caption_embeddings(
    caption_stream: AsyncIterator[dict],
    api_key: Optional[str] = None,
    model: str = OPENAI_EMBEDDING_MODEL_ID,
    store: Optional[CaptionEmbeddingStore] = None,
) -> AsyncIterator[dict]:
    """
    Consume a stream of captions and yield embedding results.

    For each final caption, generates an embedding using the OpenAI
    text-embedding-3-small model and optionally stores it for search.

    Args:
        caption_stream: Async iterator yielding dicts with 'text' and 'is_final' keys.
        api_key: OpenAI API key.
        model: OpenAI embedding model identifier.
        store: Optional CaptionEmbeddingStore for persistence.

    Yields:
        dict: CaptionEmbedding data with text, vector, and metadata.
    """
    embedder = CaptionEmbedder(api_key=api_key, model=model)
    index = 0
    local_store = store or CaptionEmbeddingStore()

    async for caption in caption_stream:
        text = caption.get("text", "")
        is_final = caption.get("is_final", False)
        timestamp_ms = caption.get("timestamp_ms", 0.0)

        if is_final and text.strip():
            embedding_vec = await embedder.embed_text(text)
            if embedding_vec:
                cap_emb = CaptionEmbedding(
                    text=text,
                    embedding=embedding_vec,
                    index=index,
                    timestamp_ms=timestamp_ms,
                    is_final=is_final,
                    model=model,
                )
                local_store.add(cap_emb)
                index += 1
                yield cap_emb.to_dict()
