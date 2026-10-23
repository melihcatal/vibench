import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import OpenAI

from embeddings_models import BatchEmbeddingRequest, EmbeddingRequest


@dataclass
class EmbeddingsClient:
    client: OpenAI

    def create_embedding(self, request: EmbeddingRequest) -> Dict[str, Any]:
        return self.client.embeddings.create(input=request.input, model=request.model).model_dump()

    def create_embeddings(self, request: BatchEmbeddingRequest) -> Dict[str, Any]:
        return self.client.embeddings.create(input=request.inputs, model=request.model).model_dump()


def create_embeddings_client(api_key: Optional[str] = None) -> EmbeddingsClient:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return EmbeddingsClient(client=OpenAI(api_key=key))
