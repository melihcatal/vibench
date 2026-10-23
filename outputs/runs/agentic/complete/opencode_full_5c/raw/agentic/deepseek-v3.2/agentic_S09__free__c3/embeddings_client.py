import os
from typing import Optional, Dict, Any
from openai import OpenAI


class EmbeddingsClient:
    """Client helper utilities for OpenAI embeddings API."""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"
    ):
        """
        Initialize the embeddings client.

        Args:
            api_key: OpenAI API key. If None, reads from OPENAI_API_KEY environment variable.
            model: The embedding model to use (default: text-embedding-3-small)
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def get_client(self) -> OpenAI:
        """Get the OpenAI client instance."""
        return self.client

    def validate_model(self, model: Optional[str] = None) -> str:
        """
        Validate and return the model to use.

        Args:
            model: Optional model override

        Returns:
            str: Validated model name
        """
        return model or self.model

    def get_available_models(self) -> list:
        """Get list of available embedding models from OpenAI."""
        # Note: OpenAI doesn't have a dedicated endpoint for listing embedding models
        # These are the commonly available embedding models
        return [
            "text-embedding-3-small",
            "text-embedding-3-large",
            "text-embedding-ada-002",
        ]

    def get_model_dimensions(self, model: Optional[str] = None) -> int:
        """
        Get the dimensionality of a specific embedding model.

        Args:
            model: Model name (default: current client model)

        Returns:
            int: Dimension count
        """
        model_name = model or self.model

        dimension_map = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }

        if model_name in dimension_map:
            return dimension_map[model_name]
        else:
            # Default to 1536 for unknown models
            return 1536

    @staticmethod
    def load_config_from_env() -> Dict[str, Any]:
        """
        Load configuration from environment variables.

        Returns:
            Dict with configuration values
        """
        config = {
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "model": os.environ.get("EMBEDDINGS_MODEL", "text-embedding-3-small"),
            "base_url": os.environ.get("OPENAI_BASE_URL"),
            "timeout": int(os.environ.get("OPENAI_TIMEOUT", "30")),
            "max_retries": int(os.environ.get("OPENAI_MAX_RETRIES", "3")),
        }
        return config
