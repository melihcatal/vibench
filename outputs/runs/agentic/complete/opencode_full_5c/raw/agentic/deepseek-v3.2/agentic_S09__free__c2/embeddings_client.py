import os
from typing import Optional, Dict, Any
from openai import OpenAI


class EmbeddingsClient:
    """Client helper utilities for OpenAI Embeddings API."""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"
    ):
        """
        Initialize the embeddings client.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
            model: The embedding model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def get_client(self) -> OpenAI:
        """Get the OpenAI client instance."""
        return self.client

    def validate_text(self, text: str, max_length: int = 8192) -> bool:
        """
        Validate text before embedding.

        Args:
            text: Text to validate
            max_length: Maximum allowed text length

        Returns:
            bool: True if text is valid
        """
        if not text or not isinstance(text, str):
            return False
        if len(text.strip()) == 0:
            return False
        if len(text) > max_length:
            return False
        return True

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current embedding model."""
        model_info = {
            "model": self.model,
            "provider": "OpenAI",
            "dimensions": self._get_model_dimensions(),
            "max_input_length": 8192,
        }

        if self.model.startswith("text-embedding-3"):
            model_info["dimensions"] = 1536
            model_info["family"] = "text-embedding-3"
        elif self.model.startswith("text-embedding-ada-002"):
            model_info["dimensions"] = 1536
            model_info["family"] = "text-embedding-ada-002"

        return model_info

    def _get_model_dimensions(self) -> int:
        """Get the dimensions for the current model."""
        if self.model.startswith("text-embedding-3"):
            return 1536
        elif self.model.startswith("text-embedding-ada-002"):
            return 1536
        else:
            # Default for unknown models
            return 1536

    @staticmethod
    def normalize_embedding(embedding: list) -> list:
        """
        Normalize an embedding vector to unit length.

        Args:
            embedding: The embedding vector

        Returns:
            list: Normalized embedding vector
        """
        import numpy as np

        vec = np.array(embedding)
        norm = np.linalg.norm(vec)
        if norm == 0:
            return embedding
        normalized = vec / norm
        return normalized.tolist()
