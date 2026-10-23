import os
from typing import Optional, Dict, Any
from openai import OpenAI


class EmbeddingsClient:
    """Client helper utilities for OpenAI Embeddings API."""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")

        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def get_client(self) -> OpenAI:
        """Get the OpenAI client instance."""
        return self.client

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the embedding model being used."""
        return {
            "provider": "OpenAI",
            "model": self.model,
            "dimensions": 1536 if self.model == "text-embedding-3-small" else 3072,
            "max_tokens": 8191,
        }

    def validate_text_length(self, text: str) -> bool:
        """Validate that text length is within model limits."""
        token_count = len(text.split())  # Simple approximation
        return token_count <= 8191

    @staticmethod
    def load_config() -> Dict[str, str]:
        """Load configuration from environment variables."""
        config = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
            "OPENAI_EMBEDDING_MODEL": os.getenv(
                "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
            ),
        }
        return config
