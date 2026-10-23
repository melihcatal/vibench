"""
Local configuration and client helper utilities for Direct Embeddings API.

Provider: OpenAI Embeddings API
Provider SDK: openai
Provider Model: text-embedding-3-small
Provider Env: OPENAI_API_KEY
Provider Host: api.openai.com
"""

import os
from typing import Optional

from openai import OpenAI


_DEFAULT_MODEL = "text-embedding-3-small"
_DEFAULT_DIMENSIONS = 1536


class EmbeddingsClient:
    """Helper client wrapping OpenAI embeddings integration."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = _DEFAULT_MODEL,
        dimensions: int = _DEFAULT_DIMENSIONS,
        organization: Optional[str] = None,
    ) -> None:
        self._model = model
        self._dimensions = dimensions
        self._client = OpenAI(
            api_key=api_key or os.environ.get("OPENAI_API_KEY"),
            organization=organization,
        )

    @property
    def client(self) -> OpenAI:
        return self._client

    @property
    def model(self) -> str:
        return self._model

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, text: str, dimensions: Optional[int] = None) -> list[float]:
        dim = dimensions or self._dimensions
        response = self._client.embeddings.create(
            model=self._model,
            input=text,
            dimensions=dim,
        )
        return response.data[0].embedding

    def embed_many(
        self, texts: list[str], dimensions: Optional[int] = None
    ) -> list[list[float]]:
        dim = dimensions or self._dimensions
        response = self._client.embeddings.create(
            model=self._model,
            input=texts,
            dimensions=dim,
        )
        ordered = sorted(response.data, key=lambda d: d.index)
        return [item.embedding for item in ordered]

    def get_usage_info(self, response) -> dict:
        return {
            "model": response.model,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }
