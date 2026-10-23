import os
import openai
from typing import List

class EmbeddingsClient:
    def __init__(self, api_key: str = None, model: str = "text-embedding-3-small"):
        self.api_key = api_key if api_key else os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model

    def get_embedding(self, text: str) -> List[float]:
        response = self.client.embeddings.create(input=[text], model=self.model)
        return response.data[0].embedding

    def get_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(input=texts, model=self.model)
        return [d.embedding for d in response.data]
