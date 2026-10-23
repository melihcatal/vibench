from typing import List, Optional
import os
import numpy as np
from openai import OpenAI
from .embeddings_models import EmbeddingRequest, EmbeddingResponse


class EmbeddingsClient:
    def __init__(
        self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def embed(
        self, texts: List[str], dimensions: Optional[int] = None
    ) -> EmbeddingResponse:
        if not isinstance(texts, list):
            raise ValueError("Input must be a list of strings")

        request = {"input": texts, "model": self.model}
        if dimensions:
            request["dimensions"] = dimensions

        response = self.client.embeddings.create(**request)
        return EmbeddingResponse(
            embeddings=[data.embedding for data in response.data],
            model=response.model,
            usage=response.usage,
        )
