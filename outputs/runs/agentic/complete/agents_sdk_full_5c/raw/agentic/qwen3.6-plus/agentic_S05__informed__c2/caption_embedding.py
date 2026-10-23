"""
Embed caption chunks for semantic meeting search using OpenAI Embeddings API.
Generates vector embeddings from streaming transcript segments for semantic indexing.

Provider: OpenAI Embeddings API
SDK: openai
Auth: OPENAI_API_KEY
Model: text-embedding-3-small
"""

import logging
from typing import Optional

import numpy as np
from openai import OpenAI

from speech_models import FinalTranscriptResult

logger = logging.getLogger(__name__)


class CaptionEmbedder:
    """
    Embeds caption chunks for semantic search using OpenAI Embeddings API.

    Converts transcript segments into dense vector representations suitable
    for semantic similarity search and meeting content indexing.
    """

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
        dimensions: Optional[int] = None,
    ):
        """
        Initialize the OpenAI caption embedder.

        Args:
            model: OpenAI embedding model (e.g., 'text-embedding-3-small', 'text-embedding-3-large').
            api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
            dimensions: Optional output dimensionality (for supported models).
        """
        self.model = model
        self.dimensions = dimensions

        openai_key = api_key
        if not openai_key:
            import os
            openai_key = os.environ.get("OPENAI_API_KEY")

        self.client = OpenAI(api_key=openai_key)
        self._embedding_store: list[dict] = []

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding vector for a text string using OpenAI API.

        Args:
            text: Text to embed.

        Returns:
            List of floats representing the embedding vector.
        """
        if not text or not text.strip():
            return []

        try:
            params = {
                "model": self.model,
                "input": text,
            }
            if self.dimensions:
                params["dimensions"] = self.dimensions

            response = self.client.embeddings.create(**params)
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenAI embedding error: {e}")
            return []

    def embed_final_result(self, result: FinalTranscriptResult) -> dict:
        """
        Embed a FinalTranscriptResult and store it with metadata.

        Args:
            result: FinalTranscriptResult to embed.

        Returns:
            Dict with text, embedding, and metadata.
        """
        embedding = self.embed_text(result.transcript)
        entry = {
            "text": result.transcript,
            "embedding": embedding,
            "confidence": result.confidence,
            "language_code": result.language_code,
            "start_time": result.start_time_seconds,
            "end_time": result.end_time_seconds,
        }
        self._embedding_store.append(entry)
        return entry

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple text strings in a single API call.

        Args:
            texts: List of texts to embed.

        Returns:
            List of embedding vectors.
        """
        if not texts:
            return []

        filtered = [t for t in texts if t and t.strip()]
        if not filtered:
            return [[] for _ in texts]

        try:
            params = {
                "model": self.model,
                "input": filtered,
            }
            if self.dimensions:
                params["dimensions"] = self.dimensions

            response = self.client.embeddings.create(**params)
            embeddings = [d.embedding for d in response.data]
            return embeddings
        except Exception as e:
            logger.error(f"OpenAI batch embedding error: {e}")
            return [[] for _ in texts]

    def cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        """
        Compute cosine similarity between two embedding vectors.

        Args:
            vec_a: First embedding vector.
            vec_b: Second embedding vector.

        Returns:
            Cosine similarity score (0.0 to 1.0).
        """
        if not vec_a or not vec_b:
            return 0.0

        a = np.array(vec_a)
        b = np.array(vec_b)

        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(np.dot(a, b) / (norm_a * norm_b))

    def search_similar(
        self,
        query_text: str,
        top_k: int = 5,
        min_similarity: float = 0.5,
    ) -> list[dict]:
        """
        Search stored embeddings for semantically similar captions.

        Args:
            query_text: Query text to search for.
            top_k: Number of top results to return.
            min_similarity: Minimum similarity threshold.

        Returns:
            List of matching entries sorted by similarity.
        """
        query_embedding = self.embed_text(query_text)
        if not query_embedding:
            return []

        results = []
        for entry in self._embedding_store:
            if not entry.get("embedding"):
                continue
            similarity = self.cosine_similarity(query_embedding, entry["embedding"])
            if similarity >= min_similarity:
                results.append({**entry, "similarity": similarity})

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def get_store(self) -> list[dict]:
        """Return all stored embeddings with metadata."""
        return list(self._embedding_store)

    def clear_store(self) -> None:
        """Clear the embedding store."""
        self._embedding_store.clear()


def create_embedder(
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> CaptionEmbedder:
    """
    Factory function to create an OpenAI caption embedder.

    Args:
        model: OpenAI embedding model.
        api_key: OpenAI API key.
        dimensions: Optional output dimensionality.

    Returns:
        Configured CaptionEmbedder instance.
    """
    return CaptionEmbedder(
        model=model,
        api_key=api_key,
        dimensions=dimensions,
    )
