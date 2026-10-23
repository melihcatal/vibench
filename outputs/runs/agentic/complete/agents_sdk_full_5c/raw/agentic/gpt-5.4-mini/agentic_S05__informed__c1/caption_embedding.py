from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionChunk, EmbeddingResult, chunk_text


class CaptionEmbedder:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    def embed(self, chunks: list[CaptionChunk]) -> EmbeddingResult:
        text = chunk_text(chunks)
        response = self.client.embeddings.create(model=self.model, input=text)
        vector = list(response.data[0].embedding)
        return EmbeddingResult(vector=vector, dimension=len(vector), raw={"model": self.model})
