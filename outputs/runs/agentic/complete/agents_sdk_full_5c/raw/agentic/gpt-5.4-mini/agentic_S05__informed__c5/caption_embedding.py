from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from speech_models import EmbeddingResult, normalize_text


class CaptionEmbedder:
    def __init__(self, model: str = "text-embedding-3-small") -> None:
        self.client = OpenAI()
        self.model = model

    def embed_text(self, text: str) -> EmbeddingResult:
        text = normalize_text(text)
        response = self.client.embeddings.create(model=self.model, input=text)
        vector = list(response.data[0].embedding)
        return EmbeddingResult(text=text, vector=vector, dimensions=len(vector), raw={"model": self.model})

    def embed_chunks(self, chunks: Iterable[str]) -> List[EmbeddingResult]:
        return [self.embed_text(chunk) for chunk in chunks]
