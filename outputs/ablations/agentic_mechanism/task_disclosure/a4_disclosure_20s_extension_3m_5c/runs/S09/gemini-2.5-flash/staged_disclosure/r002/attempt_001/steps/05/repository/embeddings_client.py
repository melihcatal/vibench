
import os
import requests
from typing import List, Dict, Any

class EmbeddingsClient:
    def __init__(self, api_key: str = None, api_endpoint: str = None):
        self.api_key = api_key if api_key else os.getenv("EMBEDDINGS_API_KEY")
        self.api_endpoint = api_endpoint if api_endpoint else os.getenv("EMBEDDINGS_API_ENDPOINT", "https://api.example.com/embeddings")

        if not self.api_key:
            raise ValueError("API Key not provided and not found in environment variables (EMBEDDINGS_API_KEY)")
        if not self.api_endpoint:
            raise ValueError("API Endpoint not provided and not found in environment variables (EMBEDDINGS_API_ENDPOINT)")

    def get_embedding(self, text: str) -> List[float]:
        """
        Retrieves the embedding for a given text using the Direct Embeddings API.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "text": text
        }
        try:
            response = requests.post(self.api_endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            return response.json().get("embedding")
        except requests.exceptions.RequestException as e:
            print(f"Error calling embeddings API: {e}")
            raise

    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Retrieves embeddings for a batch of texts using the Direct Embeddings API.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "texts": texts
        }
        try:
            response = requests.post(f"{self.api_endpoint}/batch", headers=headers, json=payload)
            response.raise_for_status()
            return response.json().get("embeddings")
        except requests.exceptions.RequestException as e:
            print(f"Error calling embeddings API (batch): {e}")
            raise

if __name__ == "__main__":
    # Example usage (requires EMBEDDINGS_API_KEY and EMBEDDINGS_API_ENDPOINT to be set in environment or passed directly)
    try:
        # For demonstration, you might set these in your environment or replace with actual values
        # os.environ["EMBEDDINGS_API_KEY"] = "your_api_key_here"
        # os.environ["EMBEDDINGS_API_ENDPOINT"] = "https://your-embeddings-api.com/v1/embed"

        client = EmbeddingsClient()

        # Example for single text embedding
        text_to_embed = "Hello, world!"
        embedding = client.get_embedding(text_to_embed)
        print(f"Embedding for '{text_to_embed}': {embedding[:5]}...") # Print first 5 elements

        # Example for batch text embeddings
        texts_to_embed = ["First sentence.", "Second sentence for embedding."]
        embeddings_batch = client.get_embeddings_batch(texts_to_embed)
        print(f"Embeddings for batch: {[e[:5] for e in embeddings_batch]}...")

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
