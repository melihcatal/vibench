from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import normalize_transcript_text


def embed_caption_chunks(
    captions: Iterable[str],
    *,
    model: str = "text-embedding-3-small",
) -> List[dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    texts = [normalize_transcript_text(c) for c in captions]
    texts = [t for t in texts if t]
    if not texts:
        return []

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=model, input=texts)
    return [
        {
            "text": text,
            "embedding": item.embedding,
            "index": item.index,
            "provider": "openai",
            "model": model,
        }
        for text, item in zip(texts, response.data)
    ]
