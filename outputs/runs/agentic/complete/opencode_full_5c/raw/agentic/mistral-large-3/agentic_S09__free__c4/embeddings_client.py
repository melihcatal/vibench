from typing import List, Optional
import numpy as np
import cohere
import os


class EmbeddingsClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")
        self.client = cohere.Client(self.api_key)

    def embed(
        self,
        texts: List[str],
        model: str = "embed-multilingual-v3.0",
        input_type: str = "search_document",
    ) -> List[List[float]]:
        response = self.client.embed(texts=texts, model=model, input_type=input_type)
        return response.embeddings
