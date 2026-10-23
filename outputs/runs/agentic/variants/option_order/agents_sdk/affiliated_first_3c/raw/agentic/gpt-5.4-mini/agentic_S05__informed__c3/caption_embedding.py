from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import TranscriptChunk


class CaptionEmbedder:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "text-embedding-3-small"

    def embed(self, text: str) -> List[float]:
        response = self.client.embeddings.create(model=self.model, input=text)
        return list(response.data[0].embedding)


def embed_caption_chunks(chunks: Iterable[TranscriptChunk]) -> List[List[float]]:
    embedder = CaptionEmbedder()
    return [embedder.embed(chunk.text) for chunk in chunks]
