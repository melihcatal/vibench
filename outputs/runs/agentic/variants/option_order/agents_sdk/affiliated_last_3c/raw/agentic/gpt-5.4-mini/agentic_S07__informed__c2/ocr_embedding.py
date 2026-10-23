from __future__ import annotations

import os
from typing import List

import openai

from document_models import EmbeddingResponse


class DocumentEmbedder:
    def __init__(self) -> None:
        self.client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def embed_sections(self, sections: List[str], model: str = "text-embedding-3-small") -> EmbeddingResponse:
        response = self.client.embeddings.create(input=sections, model=model)
        vectors = [item.embedding for item in response.data]
        return EmbeddingResponse(vectors=vectors, provider="openai", metadata={"model": model})
