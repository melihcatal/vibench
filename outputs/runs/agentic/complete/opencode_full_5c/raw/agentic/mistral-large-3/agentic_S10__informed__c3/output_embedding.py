import os
from typing import List, Optional
from cohere import Client


class OutputEmbedder:
    def __init__(self, model: Optional[str] = None):
        self.model = model or "embed-english-v3.0"
        self.client = Client(api_key=os.getenv("COHERE_API_KEY"))

    def embed(self, text: str) -> List[float]:
        response = self.client.embed(
            texts=[text], model=self.model, input_type="search_document"
        )
        return response.embeddings[0]
