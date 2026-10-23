import os
from typing import List

# Configuration parameters (to be set as environment variables)
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


class EmbeddingsModels:
    """Local helpers for request/response normalization with Direct Embeddings API.",

    This module provides utilities to convert raw SDK responses into a consistent
    format used across the integration files. The actual SDK calls are abstracted
    by the DirectEmbeddingsConfig class.",

    Args:
        service (str): Provider name (e.g., 'DashScope').
    """

    @staticmethod
    def normalize_embed_response(raw_response: dict) -> list[float]:
        """Extract embedding vector from service‑specific raw response.",

        Args:
            raw_response (dict): Raw response from the provider SDK/client.

        Returns:
            list[float]: Normalized embedding vector."
        """
        if "embedding" in raw_response:
            return raw_response["embedding"]
        # Fallback for other services (implementation omitted for brevity)
        raise ValueError("Unsupported response format")

    @staticmethod
    def sanitize_text(text: str) -> str:
        """Basic sanitization of input text before embedding.",

        This removes newlines and trims whitespace. Extend as needed for
        language‑specific preprocessing.",
        """
        return " ".join(text.split())

    @classmethod
    def batch_normalize(cls, raw_batch: List[dict]) -> List[list[float]]:
        """Normalize a batch of raw responses into a list of embedding vectors.",

        Args:
            raw_batch (List[dict]): List of raw SDK responses, one per text.

        Returns:
            List[list[float]]: List of embedding vectors.",
        """
        return [cls.normalize_embed_response(item) for item in raw_batch]
