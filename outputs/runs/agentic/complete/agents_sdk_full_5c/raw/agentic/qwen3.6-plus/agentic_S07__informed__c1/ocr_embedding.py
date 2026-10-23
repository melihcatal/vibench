"""Embed extracted document sections for semantic retrieval using OpenAI Embeddings."""

import os
from openai import OpenAI

from document_models import EmbeddingRequest, EmbeddingResponse


class OpenAIEmbedder:
    """Text embedding via OpenAI Embeddings SDK."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.api_key)

    def embed_texts(
        self,
        texts: list[str],
        model: str = "text-embedding-3-small",
    ) -> EmbeddingResponse:
        """Generate embeddings for a list of text strings using OpenAI."""
        if not self.api_key:
            raise EnvironmentError("Missing OPENAI_API_KEY environment variable.")

        response = self.client.embeddings.create(
            input=texts,
            model=model,
        )

        embeddings = []
        for item in response.data:
            embeddings.append(item.embedding)

        return EmbeddingResponse(
            embeddings=embeddings,
            model=model,
            provider="openai",
        )

    def embed_single(
        self,
        text: str,
        model: str = "text-embedding-3-small",
    ) -> list[float]:
        """Generate embedding for a single text string using OpenAI."""
        response = self.embed_texts([text], model=model)
        return response.embeddings[0] if response.embeddings else []


def embed_document_sections(sections: list[str], model: str = "text-embedding-3-small") -> EmbeddingResponse:
    """High-level helper: embed extracted document sections via OpenAI Embeddings."""
    embedder = OpenAIEmbedder()
    return embedder.embed_texts(sections, model=model)


def embed_single_section(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """High-level helper: embed a single document section via OpenAI Embeddings."""
    embedder = OpenAIEmbedder()
    return embedder.embed_single(text, model=model)
