from __future__ import annotations

import os
from typing import Iterable

import cohere


class CaptionEmbedder:
    def __init__(self, model: str = "embed-v4.0") -> None:
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise RuntimeError("COHERE_API_KEY is required")
        self.client = cohere.ClientV2(api_key=api_key)
        self.model = model

    def embed_chunks(self, caption_chunks: Iterable[str]) -> list[list[float]]:
        texts = [chunk.strip() for chunk in caption_chunks if chunk and chunk.strip()]
        if not texts:
            return []
        response = self.client.embed(
            model=self.model,
            input_type="search_document",
            embedding_types=["float"],
            texts=texts,
        )
        return response.embeddings.float
