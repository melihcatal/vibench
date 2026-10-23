import os
import openai
from typing import List, Dict, Any
from embeddings_models import EmbeddingRequest, EmbeddingResponse

class EmbeddingsClient:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def get_embeddings(self, texts: List[str], model: str) -> EmbeddingResponse:
        response = self.client.embeddings.create(input=texts, model=model)
        return EmbeddingResponse(
            object=response.object,
            data=[item.model_dump() for item in response.data],
            model=response.model,
            usage=response.usage.model_dump()
        )
