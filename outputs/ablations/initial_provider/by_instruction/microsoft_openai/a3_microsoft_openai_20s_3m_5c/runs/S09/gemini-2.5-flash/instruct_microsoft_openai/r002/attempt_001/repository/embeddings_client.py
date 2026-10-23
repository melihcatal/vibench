import os
import openai
from typing import List, Dict, Any
from embeddings_models import EmbeddingRequest, EmbeddingResponse

class EmbeddingsClient:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def create_embeddings(self, request: EmbeddingRequest) -> EmbeddingResponse:
        response = self.client.embeddings.create(input=request.texts, model=request.model)
        return EmbeddingResponse(
            data=[{"embedding": r.embedding, "index": r.index, "object": r.object} for r in response.data],
            model=response.model
        )
