import os
from typing import Optional

# Example: configuration for DashScope embeddings service
# The service requires an API key stored in DASHSCOPE_API_KEY environment variable


class EmbeddingsClient:
    """Local helper client for Direct Embeddings API.

    Loads configuration and provides utility methods shared across integration files.
    """

    def __init__(self, api_key: Optional[str] = None):
        # Prefer explicit key passed to constructor, otherwise fall back to env var
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable not set")
        # SDK client could be instantiated here if required for reuse
        # self.client = dashscope.Client(api_key=self.api_key)

    def get_api_key(self) -> str:
        """Return the configured API key."""
        return self.api_key

    def normalize_text(self, text: str) -> str:
        """Simple normalization: strip whitespace and lower-case.
        Extend as needed for your use case.
        """
        return text.strip().lower()
