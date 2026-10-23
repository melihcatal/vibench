from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from speech_models import CaptionSegment, normalize_transcript_text


def embed_caption_chunks(chunks: Iterable[CaptionSegment]) -> List[List[float]]:
    client = OpenAI(api_key=None)
    texts = [
        normalize_transcript_text(chunk.text)
        for chunk in chunks
        if normalize_transcript_text(chunk.text)
    ]
    if not texts:
        return []
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    return [item.embedding for item in response.data]
