import os
from typing import Optional

import cohere
from cohere import Client as CohereClient


class EmbeddingsClient:
    """Client helper for Cohere Embeddings API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")
        self.client = CohereClient(self.api_key)

    def get_client(self) -> CohereClient:
        return self.client