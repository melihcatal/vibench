import os
from typing import Optional
from openai import OpenAI


class EmbeddingsClient:
    """Client helper for OpenAI embeddings API with configuration management."""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"
    ):
        """
        Initialize the embeddings client.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
            model: Default embedding model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be provided or set in environment")

        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def get_client(self) -> OpenAI:
        """Get the OpenAI client instance."""
        return self.client

    def validate_model(self, model: str) -> bool:
        """Validate if a model name is likely a valid OpenAI embedding model."""
        valid_prefixes = ["text-embedding-", "text-search-"]
        return any(model.startswith(prefix) for prefix in valid_prefixes)

    @staticmethod
    def get_available_models() -> list[str]:
        """Get list of available OpenAI embedding models."""
        return [
            "text-embedding-3-small",
            "text-embedding-3-large",
            "text-embedding-ada-002",
        ]

    @staticmethod
    def get_model_dimensions(model: str) -> int:
        """Get the embedding dimensions for a given model."""
        dimensions_map = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
        return dimensions_map.get(model, 1536)
