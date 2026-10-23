from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import CaptionChunk, normalize_transcript_text


class CaptionEmbeddingIndex:
    def __init__(self, model: str = "text-embedding-3-small") -> None:
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_chunk(self, chunk: CaptionChunk) -> List[float]:
        text = normalize_transcript_text(chunk.text)
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )
        return list(response.data[0].embedding)

    def embed_many(self, chunks: Iterable[CaptionChunk]) -> List[List[float]]:
        texts = [normalize_transcript_text(chunk.text) for chunk in chunks]
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [list(item.embedding) for item in response.data]
