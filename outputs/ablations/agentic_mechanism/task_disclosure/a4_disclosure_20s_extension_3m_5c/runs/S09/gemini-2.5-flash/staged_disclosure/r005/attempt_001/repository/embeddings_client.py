
import os
import requests
from typing import List, Dict, Any

class EmbeddingsClient:
    def __init__(self, api_key: str = None, api_endpoint: str = None):
        """
        Initializes the EmbeddingsClient with API key and endpoint.
        Uses environment variables if not provided.
        """
        self.api_key = api_key or os.environ.get("EMBEDDINGS_API_KEY")
        self.api_endpoint = api_endpoint or os.environ.get("EMBEDDINGS_API_ENDPOINT", "https://api.example.com/embeddings")

        if not self.api_key:
            raise ValueError("API key not provided. Set EMBEDDINGS_API_KEY environment variable or pass it to the constructor.")
        if not self.api_endpoint:
            raise ValueError("API endpoint not provided. Set EMBEDDINGS_API_ENDPOINT environment variable or pass it to the constructor.")

    def create_embeddings(self, texts: List[str]) -> Dict[str, Any]:
        """
        Calls the Direct Embeddings API to generate embeddings for a list of texts.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "texts": texts
        }

        try:
            response = requests.post(self.api_endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating embeddings: {e}")
            raise
