from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from speech_models import CaptionChunk, join_caption_chunks


class CaptionEmbedder:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def embed(self, chunks: List[CaptionChunk]) -> list[float]:
        text = join_caption_chunks(chunks)
        response = self.client.embeddings.create(model="text-embedding-3-small", input=text)
        return list(response.data[0].embedding)
