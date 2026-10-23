# Local configuration and client utilities for Direct Embeddings API
# Example provider: OpenAI (adjust API key and endpoint as needed)

import os
import json
import requests


class EmbeddingsClient:
    """Client to interact with Direct Embeddings API."""

    def __init__(self, api_key=None, base_url="https://api.openai.com/v1/embeddings"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "OpenAI API key not found. Set OPENAI_API_KEY env var or pass directly."
            )
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.base_url = base_url

    def create_embedding(self, model: str, input: str | list) -> dict:
        """Call the embeddings endpoint and return JSON response."""
        payload = {"model": model, "input": input}
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        if response.status_code != 200:
            raise RuntimeError(
                f"Embeddings API error: {response.status_code} {response.text}"
            )
        return response.json()

    def normalize_embedding(self, embedding: list) -> list:
        """Ensure embedding is a list of floats and clip to reasonable range."""
        return [float(x) for x in embedding]

    def batch_normalize(self, batch: list) -> list:
        """Normalize a list of embeddings."""
        return [self.normalize_embedding(e) for e in batch]
