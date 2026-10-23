import os
from openai import OpenAI
from typing import List, Dict, Any
from embeddings_models import EmbeddingRequest, BatchEmbeddingRequest, EmbeddingResponse, BatchEmbeddingResponse

class EmbeddingsClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            # You can also set OPENAI_API_BASE for Azure OpenAI Service
            # base_url=os.environ.get("OPENAI_API_BASE_URL") 
        )
        self.default_model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

    def get_embedding(self, request: EmbeddingRequest) -> EmbeddingResponse:
        response = self.client.embeddings.create(
            model=request.model or self.default_model,
            input=request.text
        )
        return EmbeddingResponse(
            embedding=response.data[0].embedding,
            model=response.model,
            usage=response.usage.model_dump()
        )

    def get_batch_embeddings(self, request: BatchEmbeddingRequest) -> BatchEmbeddingResponse:
        response = self.client.embeddings.create(
            model=request.model or self.default_model,
            input=request.texts
        )
        return BatchEmbeddingResponse(
            embeddings=[d.embedding for d in response.data],
            model=response.model,
            usage=response.usage.model_dump()
        )
