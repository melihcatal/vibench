import os
from typing import Optional, Dict, Any
from openai import OpenAI


class EmbeddingsClient:
    """Client helper utilities for OpenAI embeddings API."""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def get_embedding(self, text: str) -> list[float]:
        """Get embedding for a single text."""
        response = self.client.embeddings.create(
            model=self.model, input=text, encoding_format="float"
        )
        return response.data[0].embedding

    def get_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings for multiple texts."""
        response = self.client.embeddings.create(
            model=self.model, input=texts, encoding_format="float"
        )
        return [item.embedding for item in response.data]

    @staticmethod
    def validate_text(text: str, max_length: int = 8192) -> bool:
        """Validate text length for embedding API."""
        return len(text) <= max_length

    @staticmethod
    def get_available_models() -> list[str]:
        """Return available OpenAI embedding models."""
        return [
            "text-embedding-3-small",
            "text-embedding-3-large",
            "text-embedding-ada-002",
        ]
