import os
from openai import OpenAI
from typing import List, Union


class EmbeddingsClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=api_key)
        self.model = "text-embedding-3-small"

    def embed_documents(self, texts: List[str]) -> List[list[float]]:
        if not texts:
            return []
        response = self.client.embeddings.create(input=texts, model=self.model)
        return [data.embedding for data in response.data]
