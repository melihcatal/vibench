import os
from typing import List

import openai


class TranslationMemoryEmbedder:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    def embed(self, segments: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(model=self.model, input=segments)
        return [item.embedding for item in response.data]


def translation_memory_embedding(segments: List[str]) -> List[List[float]]:
    return TranslationMemoryEmbedder().embed(segments)
