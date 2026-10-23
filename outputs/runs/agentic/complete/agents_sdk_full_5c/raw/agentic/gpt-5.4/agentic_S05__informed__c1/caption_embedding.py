from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import CaptionEmbeddingResult, normalize_transcript_text


EMBEDDING_MODEL = "text-embedding-3-small"


def embed_caption_chunks(chunks: Iterable[str]) -> List[CaptionEmbeddingResult]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY for OpenAI embeddings")
    client = OpenAI(api_key=api_key)
    texts = [normalize_transcript_text(chunk) for chunk in chunks if normalize_transcript_text(chunk)]
    if not texts:
        return []
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    results: List[CaptionEmbeddingResult] = []
    for text, item in zip(texts, response.data):
        results.append(
            CaptionEmbeddingResult(
                text=text,
                embedding=list(item.embedding),
                model=EMBEDDING_MODEL,
                raw={"provider": "OpenAI", "index": item.index},
            )
        )
    return results
