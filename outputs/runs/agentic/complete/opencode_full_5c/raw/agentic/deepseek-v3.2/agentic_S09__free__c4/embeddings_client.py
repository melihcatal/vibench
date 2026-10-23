import os
from typing import Optional, Dict, Any
from openai import OpenAI


class EmbeddingsClient:
    """Client helper utilities for OpenAI embeddings API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the embeddings client.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
            base_url: Optional custom base URL for the API
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        client_kwargs = {"api_key": self.api_key}
        if base_url:
            client_kwargs["base_url"] = base_url

        self.client = OpenAI(**client_kwargs)

    def get_available_models(self) -> list:
        """Get list of available embedding models from OpenAI."""
        try:
            models = self.client.models.list()
            embedding_models = [
                model.id
                for model in models.data
                if "embedding" in model.id.lower()
                or model.id.startswith("text-embedding")
            ]
            return sorted(embedding_models)
        except Exception as e:
            print(f"Error fetching models: {e}")
            return [
                "text-embedding-3-small",
                "text-embedding-3-large",
                "text-embedding-ada-002",
            ]

    def validate_text_length(
        self, text: str, model: str = "text-embedding-3-small"
    ) -> bool:
        """
        Validate text length for the embedding model.

        Args:
            text: Text to validate
            model: Model identifier

        Returns:
            True if text length is acceptable
        """
        max_tokens = 8191 if "3-small" in model or "3-large" in model else 8191

        token_count = len(text.split())
        estimated_tokens = token_count * 1.3

        return estimated_tokens <= max_tokens

    def get_model_dimensions(self, model: str) -> int:
        """
        Get embedding dimensions for a specific model.

        Args:
            model: Model identifier

        Returns:
            Number of dimensions in the embedding
        """
        model_dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }

        return model_dimensions.get(model, 1536)
