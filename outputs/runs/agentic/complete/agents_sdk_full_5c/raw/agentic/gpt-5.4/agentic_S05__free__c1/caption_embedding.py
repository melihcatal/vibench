from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from speech_models import normalize_whitespace


def embed_caption_chunks(
    caption_chunks: Iterable[str],
    *,
    model: str = "text-embedding-3-small",
) -> List[List[float]]:
    client = OpenAI()
    prepared = [normalize_whitespace(chunk) for chunk in caption_chunks if normalize_whitespace(chunk)]
    if not prepared:
        return []
    response = client.embeddings.create(
        model=model,
        input=prepared,
    )
    return [item.embedding for item in response.data]
