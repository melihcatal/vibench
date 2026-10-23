from __future__ import annotations

import os
from typing import Iterable

from openai import AsyncOpenAI

from speech_models import TranscriptChunk


async def embed_caption_chunks(chunks: Iterable[TranscriptChunk]) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI embeddings")
    texts = [chunk.text for chunk in chunks if chunk.text.strip()]
    client = AsyncOpenAI(api_key=api_key)
    response = await client.embeddings.create(
        model="text-embedding-3-large", input=texts
    )
    return {
        "provider": "openai",
        "model": "text-embedding-3-large",
        "items": [
            {"text": text, "embedding": item.embedding}
            for text, item in zip(texts, response.data)
        ],
    }
