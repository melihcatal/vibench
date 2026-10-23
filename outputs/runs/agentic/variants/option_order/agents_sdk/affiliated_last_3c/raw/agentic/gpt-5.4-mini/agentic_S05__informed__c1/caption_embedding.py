from __future__ import annotations

from openai import OpenAI

from speech_models import EmbeddingResult


class CaptionEmbedder:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = OpenAI()
        self.model = model

    def embed(self, text: str) -> EmbeddingResult:
        response = self.client.embeddings.create(model=self.model, input=text)
        vector = response.data[0].embedding
        return EmbeddingResult(text=text, vector=vector, raw=response.model_dump())
