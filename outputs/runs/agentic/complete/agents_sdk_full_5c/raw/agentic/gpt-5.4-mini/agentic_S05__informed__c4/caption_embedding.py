from __future__ import annotations

from typing import Iterable, List, Optional

from openai import OpenAI

from speech_models import EmbeddingVector, normalize_transcript_text

EMBEDDING_MODEL = "text-embedding-3-small"


class CaptionEmbedder:
    def __init__(self, api_key: Optional[str] = None) -> None:
        import os

        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def embed_chunk(self, text: str) -> EmbeddingVector:
        response = self.client.embeddings.create(model=EMBEDDING_MODEL, input=normalize_transcript_text(text))
        vector = response.data[0].embedding
        return EmbeddingVector(values=list(vector), dimensions=len(vector))


def embed_caption_chunks(chunks: Iterable[str]) -> List[EmbeddingVector]:
    embedder = CaptionEmbedder()
    return [embedder.embed_chunk(chunk) for chunk in chunks if normalize_transcript_text(chunk)]
