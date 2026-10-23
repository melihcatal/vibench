from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import EmbeddingResult, normalize_text


class CaptionEmbedder:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    def embed(self, caption: str) -> EmbeddingResult:
        text = normalize_text(caption)
        response = self.client.embeddings.create(model=self.model, input=text)
        return EmbeddingResult(vector=list(response.data[0].embedding), raw=response)

    def embed_many(self, captions: Iterable[str]) -> List[EmbeddingResult]:
        return [self.embed(c) for c in captions]
