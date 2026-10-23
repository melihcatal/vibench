from __future__ import annotations

from typing import List

from speech_models import normalize_caption


class CaptionEmbedder:
    def __init__(self) -> None:
        from openai import OpenAI  # provider-identifying import

        self.client = OpenAI()
        self.model = "text-embedding-3-small"

    def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        vectors: List[List[float]] = []
        for chunk in chunks:
            text = normalize_caption(chunk)
            if not text:
                continue
            response = self.client.embeddings.create(model=self.model, input=text)
            vectors.append(response.data[0].embedding)
        return vectors
