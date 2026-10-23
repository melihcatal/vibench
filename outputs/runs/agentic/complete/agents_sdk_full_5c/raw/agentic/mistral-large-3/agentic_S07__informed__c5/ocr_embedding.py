import os
from typing import List
import cohere


class OCREmbedder:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        self.client = cohere.Client(self.api_key)

    def embed_text(self, text: str) -> List[float]:
        response = self.client.embed(texts=[text], model="embed-english-v3.0")
        return response.embeddings[0]