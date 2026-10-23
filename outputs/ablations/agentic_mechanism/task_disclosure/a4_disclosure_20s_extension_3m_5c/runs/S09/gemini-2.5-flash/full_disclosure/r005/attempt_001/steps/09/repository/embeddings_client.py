import os
import requests
import json

class EmbeddingsClient:
    def __init__(self, api_key: str = None, api_endpoint: str = None):
        self.api_key = api_key or os.getenv("EMBEDDINGS_API_KEY")
        self.api_endpoint = api_endpoint or os.getenv("EMBEDDINGS_API_ENDPOINT", "https://api.embeddings.example.com/v1/embed")

        if not self.api_key:
            raise ValueError("API key not provided. Set EMBEDDINGS_API_KEY environment variable or pass it to the constructor.")

    def _make_request(self, texts: list[str]) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "texts": texts
        }
        try:
            response = requests.post(self.api_endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making embeddings request: {e}")
            raise

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        response_data = self._make_request(texts)
        # Assuming the API returns embeddings in a specific format, e.g., {"embeddings": [[...], [...]]}
        if "embeddings" in response_data:
            return response_data["embeddings"]
        else:
            raise ValueError("Unexpected response format from embeddings API.")
