import os


class DirectEmbeddingsClient:
    def __init__(self):
        self.api_key = os.getenv("DIRECT_EMBEDDINGS_API_KEY")
        self.base_url = "https://api.directembeddings.com/v1"

    def embed_text(self, text: str):
        response = self._make_request("POST", "/embed", json={"text": text})
        return EmbeddingsResponse(response)

    def embed_batch(self, texts: list):
        response = self._make_request("POST", "/embed_batch", json={"texts": texts})
        return EmbeddingsResponse(response)

    @staticmethod
    def cosine_similarity(embedding1, embedding2):
        import numpy as np

        return np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )

    def _make_request(self, method, endpoint, **kwargs):
        import requests

        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()
