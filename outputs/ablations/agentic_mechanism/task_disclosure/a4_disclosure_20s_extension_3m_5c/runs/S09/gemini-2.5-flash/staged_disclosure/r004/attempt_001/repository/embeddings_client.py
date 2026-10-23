import os
import requests

class EmbeddingsClient:
    def __init__(self, api_key: str = None, base_url: str = "https://api.example.com/embeddings"):
        self.api_key = api_key or os.getenv("EMBEDDINGS_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided and EMBEDDINGS_API_KEY environment variable not set.")
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_embedding(self, text: str):
        payload = {"text": text}
        try:
            response = requests.post(f"{self.base_url}/create", headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating embedding: {e}")
            return None

    def get_embedding_status(self, embedding_id: str):
        try:
            response = requests.get(f"{self.base_url}/{embedding_id}/status", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting embedding status: {e}")
            return None
