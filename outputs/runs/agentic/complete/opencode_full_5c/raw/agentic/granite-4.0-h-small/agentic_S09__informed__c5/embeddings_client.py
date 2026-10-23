# [HELPER] embeddings_client.py
# Local configuration and client helper utilities for Direct Embeddings API

# Provider: OpenAI Embeddings
# SDK: openai
# Integration signal: OPENAI_API_KEY environment variable

import os
from openai import OpenAI


class EmbeddingsClient:
    """Simple wrapper around OpenAI embeddings API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set OPENAI_API_KEY environment variable")
        self.client = OpenAI(api_key=self.api_key)

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text,
        )
        return response.data[0].embedding

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=texts,
        )
        return [item.embedding for item in response.data]
