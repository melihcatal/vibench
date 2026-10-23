import os
import requests


class EmbeddingsClient:
    def __init__(self):
        self.api_key = os.getenv("DIRECT_EMBEDDINGS_API_KEY")
        self.api_url = "https://api.directembeddings.com/v1/embeddings"

    def generate_embedding(self, text: str) -> dict:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"text": text}
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def generate_embeddings(self, texts: list[str]) -> dict:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"texts": texts}
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
