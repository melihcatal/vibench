from __future__ import annotations

from speech_client import client
from speech_models import EmbeddingResult


def caption_embedding(text: str) -> EmbeddingResult:
    return client.embed_text(text)
