import os
from typing import Dict

import dashscope

# Identifier: DashScope Embeddings SDK

dashscope.set_api_key(os.getenv("DASHSCOPE_API_KEY"))


class EmbeddingsClient:
    """Local helper to configure DashScope and provide utility methods."""

    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set DASHSCOPE_API_KEY environment variable")
        dashscope.set_api_key(self.api_key)

    def embed_text(self, text: str) -> List[float]:
        """Wrap the SDK call for a single text string."""
        resp = dashscope.embeddings.create(
            model="text-embedding-3-large",
            texts=[text],
        )
        return resp.embeddings[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Batch embedding via SDK."""
        resp = dashscope.embeddings.create(
            model="text-embedding-3-large",
            texts=texts,
        )
        return resp.embeddings
