"""Embeds caption chunks for semantic meeting search using OpenAI Embeddings API."""

import os
from typing import Optional, List
import numpy as np
import openai
from speech_models import StreamingSpeechResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_API_URL = "https://api.openai.com/v1"


class CaptionEmbedder:
    """
    Embeds caption chunks using OpenAI Embeddings API for semantic meeting search.

    Requires OPENAI_API_KEY environment variable.
    Model: text-embedding-3-small via openai SDK at api.openai.com/v1/embeddings.
    """

    def __init__(
        self,
        model: str = OPENAI_EMBEDDING_MODEL,
        api_key: Optional[str] = None,
        dimensions: Optional[int] = None,
    ):
        self.model = model
        self.dimensions = dimensions
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = openai.OpenAI(api_key=key, base_url=OPENAI_API_URL)
        self.embeddings_cache: dict[str, list[float]] = {}

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding vector for text using OpenAI embeddings API.

        Uses openai.OpenAI embeddings.create with model text-embedding-3-small.
        Endpoint: api.openai.com/v1/embeddings.
        """
        if not text.strip():
            return []
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]

        kwargs = {"input": text, "model": self.model}
        if self.dimensions:
            kwargs["dimensions"] = self.dimensions

        response = self.client.embeddings.create(**kwargs)
        embedding = response.data[0].embedding
        self.embeddings_cache[text] = embedding
        return embedding

    def embed_result(self, result: StreamingSpeechResult) -> list[float]:
        """Embed the transcript text from a streaming speech result."""
        return self.embed_text(result.transcript)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple texts in a single batch request to OpenAI Embeddings API.

        Uses openai SDK embeddings.create endpoint.
        """
        if not texts:
            return []

        kwargs = {"input": texts, "model": self.model}
        if self.dimensions:
            kwargs["dimensions"] = self.dimensions

        response = self.client.embeddings.create(**kwargs)
        embeddings = [item.embedding for item in response.data]

        for text, emb in zip(texts, embeddings):
            self.embeddings_cache[text] = emb

        return embeddings

    def search(
        self,
        query: str,
        indexed_texts: list[str],
        indexed_embeddings: list[list[float]],
        top_k: int = 5,
    ) -> list[tuple[float, str]]:
        """
        Search indexed caption embeddings semantically using cosine similarity.

        Returns list of (score, text) tuples sorted by relevance.
        """
        if not query or not indexed_embeddings:
            return []

        query_embedding = self.embed_text(query)
        query_vec = np.array(query_embedding)

        scores = []
        for text, embedding in zip(indexed_texts, indexed_embeddings):
            emb_vec = np.array(embedding)
            norm_query = np.linalg.norm(query_vec)
            norm_emb = np.linalg.norm(emb_vec)
            if norm_query == 0 or norm_emb == 0:
                similarity = 0.0
            else:
                similarity = float(np.dot(query_vec, emb_vec) / (norm_query * norm_emb))
            scores.append((similarity, text))

        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]

    def build_index(
        self,
        results: list[StreamingSpeechResult],
    ) -> tuple[list[str], list[list[float]]]:
        """
        Build an embedding index from a list of streaming speech results.

        Returns (texts, embeddings) tuple for use with search method.
        """
        texts = []
        embeddings = []
        for result in results:
            if result.transcript:
                texts.append(result.transcript)
                emb = self.embed_result(result)
                embeddings.append(emb)
        return texts, embeddings


def create_embedder(
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> CaptionEmbedder:
    """Factory to create a CaptionEmbedder using OpenAI text-embedding-3-small."""
    return CaptionEmbedder(model=model, dimensions=dimensions)
