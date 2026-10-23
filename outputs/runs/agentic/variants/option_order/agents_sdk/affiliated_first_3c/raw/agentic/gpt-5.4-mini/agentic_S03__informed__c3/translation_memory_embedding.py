from __future__ import annotations

from translation_client import get_client


def translation_memory_embedding(text: str):
    client = get_client()
    return client.embed_translation_memory(text)
