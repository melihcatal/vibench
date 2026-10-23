from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionChunk, EmbeddingResult, normalize_caption_chunks


class CaptionEmbedder:
    def __init__(self, model: str = "text-embedding-3-small") -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def embed(self, chunks: list[CaptionChunk]) -> EmbeddingResult:
        texts = [normalize_caption_chunks([chunk]) for chunk in chunks if chunk.text]
        response = self.client.embeddings.create(model=self.model, input=texts)
        vectors = [item.embedding for item in response.data]
        return EmbeddingResult(texts=texts, vectors=vectors, raw={"model": self.model})
