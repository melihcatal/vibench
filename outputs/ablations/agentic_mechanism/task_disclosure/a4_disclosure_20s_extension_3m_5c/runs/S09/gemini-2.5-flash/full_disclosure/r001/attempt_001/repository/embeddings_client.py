import os
import requests
from typing import Dict, List, Any

class EmbeddingsClient:
    def __init__(self, api_endpoint: str = None, api_key: str = None):
        self.api_endpoint = api_endpoint or os.environ.get("EMBEDDINGS_API_ENDPOINT")
        self.api_key = api_key or os.environ.get("EMBEDDINGS_API_KEY")

        if not self.api_endpoint:
            raise ValueError("API endpoint not provided or found in EMBEDDINGS_API_ENDPOINT environment variable.")
        if not self.api_key:
            raise ValueError("API key not provided or found in EMBEDDINGS_API_KEY environment variable.")

    def embed_text(self, text: str, model_id: str = "default_model") -> List[float]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "text": text,
            "model_id": model_id
        }
        try:
            response = requests.post(f"{self.api_endpoint}/embed", headers=headers, json=payload)
            response.raise_for_status()
            return response.json().get("embedding")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling embeddings API: {e}")

    def embed_batch(self, texts: List[str], model_id: str = "default_model") -> List[List[float]]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "texts": texts,
            "model_id": model_id
        }
        try:
            response = requests.post(f"{self.api_endpoint}/embed_batch", headers=headers, json=payload)
            response.raise_for_status()
            return response.json().get("embeddings")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling batch embeddings API: {e}")
