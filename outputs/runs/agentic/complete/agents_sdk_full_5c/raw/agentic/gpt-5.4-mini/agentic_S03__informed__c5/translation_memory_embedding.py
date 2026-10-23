from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from translation_models import EmbeddingResult


def embed_translated_segments(segments: Iterable[str]) -> List[EmbeddingResult]:
    client = OpenAI()
    results: List[EmbeddingResult] = []
    for segment in segments:
        response = client.embeddings.create(model="text-embedding-3-small", input=segment)
        vector = list(response.data[0].embedding)
        results.append(EmbeddingResult(text=segment, vector=vector, raw=response))
    return results
