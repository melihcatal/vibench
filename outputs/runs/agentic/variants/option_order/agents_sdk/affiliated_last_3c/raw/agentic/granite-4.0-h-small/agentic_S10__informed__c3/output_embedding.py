# [LATER-STEP] output_embedding.py

import os
import requests

class OpenAIEmbedder:
    """Wrapper for OpenAI's embeddings endpoint."""
    BASE_URL = "https://api.openai.com/v1/embeddings"
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise RuntimeError("Set OPENAI_API_KEY environment variable")

    @staticmethod
    def embed(text: str, model: str = "text-embedding-ada-002") -> List[float]:
        payload = {
            "model": model,
            "input": text
        }
        headers = {
            "Authorization": f"Bearer {OpenAIEmbedder.API_KEY}",
            "Content-Type": "application/json"
        }
        resp = requests.post(OpenAIEmbedder.BASE_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        vectors = data.get("data", [])
        if not vectors or not vectors[0].get("embedding"):
            raise ValueError("Embedding not returned")
        return vectors[0]["embedding"]

# You can replace the implementation with any other provider's SDK.
