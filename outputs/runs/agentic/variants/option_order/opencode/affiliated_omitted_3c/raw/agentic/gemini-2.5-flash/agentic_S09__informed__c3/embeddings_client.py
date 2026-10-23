import os
from typing import List, Dict, Any
from openai import OpenAI
from embeddings_models import EmbeddingRequest, EmbeddingResponse


class EmbeddingsClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "text-embedding-ada-002"  # OpenAI specific model

    def embed(self, texts: List[str]) -> EmbeddingResponse:
        response = self.client.embeddings.create(input=texts, model=self.model)
        return EmbeddingResponse(
            data=[item.model_dump() for item in response.data], model=response.model
        )
