from typing import List

from openai import OpenAI

from speech_models import normalize_text


class CaptionEmbeddingService:
    def __init__(self) -> None:
        self._client = OpenAI()

    def embed(self, caption_chunks: list[str]) -> list[list[float]]:
        inputs = [normalize_text(chunk) for chunk in caption_chunks if normalize_text(chunk)]
        if not inputs:
            return []
        response = self._client.embeddings.create(
            model="text-embedding-3-small",
            input=inputs,
        )
        return [item.embedding for item in response.data]
