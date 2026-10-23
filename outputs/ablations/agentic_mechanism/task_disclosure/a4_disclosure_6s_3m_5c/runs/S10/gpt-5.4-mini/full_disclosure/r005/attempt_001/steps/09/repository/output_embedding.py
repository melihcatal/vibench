import os
from typing import List

import requests


class OpenAIEmbeddingClient:
    def __init__(self, api_key: str | None = None, model: str = "text-embedding-3-small"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = "https://api.openai.com/v1/embeddings"

    def embed(self, outputs: List[str]) -> List[List[float]]:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")
        response = requests.post(
            self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"model": self.model, "input": outputs},
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        return [item["embedding"] for item in sorted(payload["data"], key=lambda x: x["index"])]


def embed_model_outputs(outputs: List[str], api_key: str | None = None, model: str = "text-embedding-3-small") -> List[List[float]]:
    return OpenAIEmbeddingClient(api_key=api_key, model=model).embed(outputs)
