import os
from openai import OpenAI
from typing import Optional, Dict, Any


class EmbeddingsClient:
    """Client helper for OpenAI Embeddings API."""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def get_embedding(self, text: str) -> Dict[str, Any]:
        """Get embedding for a single text."""
        response = self.client.embeddings.create(input=[text], model=self.model)
        return response.data[0].embedding

    def get_batch_embeddings(self, texts: list) -> Dict[str, Any]:
        """Get embeddings for a batch of texts."""
        response = self.client.embeddings.create(input=texts, model=self.model)
        return [data.embedding for data in response.data]
