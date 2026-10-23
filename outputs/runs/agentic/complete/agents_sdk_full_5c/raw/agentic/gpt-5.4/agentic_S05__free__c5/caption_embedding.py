import os
from typing import Optional

from openai import OpenAI

from speech_models import EmbeddingResult, normalize_transcript_text

EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


class CaptionEmbedder:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def embed(self, caption_text: str) -> EmbeddingResult:
        normalized = normalize_transcript_text(caption_text)
        response = self.client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=normalized,
        )
        return EmbeddingResult(
            text=normalized,
            vector=response.data[0].embedding,
            model=EMBEDDING_MODEL,
        )
