import os
from typing import Any, Dict

import requests

from embeddings_models import EmbeddingRequest


class DirectEmbeddingsClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, timeout: float = 30.0):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
        self.timeout = timeout

    def embed(self, request: EmbeddingRequest) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")
        url = f"{self.base_url}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = request.to_payload()
        response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
