import os
from typing import List
from openai import OpenAI
from embeddings_models import EMBEDDING_MODEL

class EmbeddingsClient:
    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY required")
        self.client = OpenAI(api_key=api_key)
        self.model = model or EMBEDDING_MODEL

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        response = self.client.embeddings.create(input=texts, model=self.model)
        return [item.embedding for item in response.data]
