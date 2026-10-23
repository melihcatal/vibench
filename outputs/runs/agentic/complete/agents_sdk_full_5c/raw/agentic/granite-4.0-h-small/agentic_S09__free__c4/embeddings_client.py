# embeddings_client.py
import os
from typing import Any

# Hypothetical provider SDK import (replace with real SDK in production)
from hypothetical_direct_embeddings_sdk import DirectEmbeddingsClient as SDKClient

class DirectEmbeddingsClient:
    """Local helper client that wraps the third‑party Direct Embeddings API SDK.",
    def __init__(self):
        # Load API key from environment or a config file
        api_key = os.getenv('DIRECT_EMBEDDINGS_API_KEY')
        if not api_key:
            raise RuntimeError('Set DIRECT_EMBEDDINGS_API_KEY env var')
        self._client = SDKClient(api_key=api_key)

    def embed(self, text: str) -> dict[str, Any]:
        """Call the API for a single text embedding.",
        return self._client.embed(text=text)

    def embed_batch(self, texts: list[str]) -> dict[str, Any]:
        """Call the API for a batch of text embeddings.",
        return self._client.embed_batch(texts=texts)