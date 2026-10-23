import os
from typing import List

from openai import OpenAI


class ModerationReasonEmbedder:
    def __init__(self, api_key: str | None = None, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def embed_reason(self, rationale: str) -> List[float]:
        response = self.client.embeddings.create(model=self.model, input=rationale)
        return response.data[0].embedding

    def embed_reasons(self, rationales: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(model=self.model, input=rationales)
        return [item.embedding for item in response.data]
