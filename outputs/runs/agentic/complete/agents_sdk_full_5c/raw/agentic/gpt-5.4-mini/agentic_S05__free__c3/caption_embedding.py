from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionRecord, normalize_caption_chunks


class CaptionEmbedder:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "text-embedding-3-small"

    def embed(self, captions: list[CaptionRecord]) -> list[list[float]]:
        texts = normalize_caption_chunks(captions)
        response = self.client.embeddings.create(model=self.model, input=texts)
        return [item.embedding for item in response.data]
