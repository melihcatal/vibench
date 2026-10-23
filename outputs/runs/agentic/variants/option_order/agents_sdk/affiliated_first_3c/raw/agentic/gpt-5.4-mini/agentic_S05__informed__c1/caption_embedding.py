from __future__ import annotations

from openai import OpenAI

from speech_models import CaptionEmbedding


class CaptionEmbedder:
    def __init__(self, model: str = "text-embedding-3-small") -> None:
        self.client = OpenAI()
        self.model = model

    def embed(self, text: str) -> CaptionEmbedding:
        response = self.client.embeddings.create(model=self.model, input=text)
        vector = list(response.data[0].embedding)
        return CaptionEmbedding(text=text, vector=vector, raw={"provider": "openai", "model": self.model, "response_id": response.id})
