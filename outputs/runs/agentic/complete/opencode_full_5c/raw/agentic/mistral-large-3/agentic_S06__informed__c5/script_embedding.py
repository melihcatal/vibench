from typing import List, Dict, Any
import os
import cohere


class CohereScriptEmbedder:
    """Embed narration scripts for voice-asset search using Cohere Embeddings."""

    def __init__(self):
        self.client = cohere.Client(os.getenv("COHERE_API_KEY"))

    def embed(self, text: str) -> List[float]:
        """Generate embeddings for the given text."""
        response = self.client.embed(texts=[text], model="embed-english-v3.0")
        return response.embeddings[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        response = self.client.embed(texts=texts, model="embed-english-v3.0")
        return response.embeddings
