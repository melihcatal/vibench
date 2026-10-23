import os
from typing import List, Optional

import cohere


class EmbeddingClient:
    """Client for Cohere Embed API."""

    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")
        self.client = cohere.Client(self.api_key)

    def embed_texts(
        self, texts: List[str], model: Optional[str] = None
    ) -> List[List[float]]:
        """Embed texts using Cohere Embed API."""
        response = self.client.embed(
            texts=texts,
            model=model or "large",
        )
        return response.embeddings


def embed_output(text: str, model: Optional[str] = None) -> List[float]:
    """Embed model output for clustering or retrieval using Cohere Embed API."""
    client = EmbeddingClient()
    embeddings = client.embed_texts([text], model)
    return embeddings[0]
