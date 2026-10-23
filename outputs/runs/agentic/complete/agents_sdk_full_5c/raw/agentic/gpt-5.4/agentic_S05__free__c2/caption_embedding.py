from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from speech_models import CaptionChunk

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_caption_chunks(chunks: Iterable[CaptionChunk], api_key: str) -> List[list[float]]:
    client = OpenAI(api_key=api_key)
    texts = [chunk.text for chunk in chunks]
    if not texts:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def embed_caption_texts(texts: Iterable[str], api_key: str) -> List[list[float]]:
    return embed_caption_chunks([CaptionChunk(text=text) for text in texts], api_key=api_key)
