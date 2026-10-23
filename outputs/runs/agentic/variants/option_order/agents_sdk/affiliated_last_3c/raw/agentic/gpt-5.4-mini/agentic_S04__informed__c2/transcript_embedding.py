from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


CLIENT = OpenAI()
MODEL = "text-embedding-3-small"


def transcript_embedding(segments: Iterable[str]) -> List[list[float]]:
    vectors: List[list[float]] = []
    for segment in segments:
        response = CLIENT.embeddings.create(model=MODEL, input=segment)
        vectors.append(response.data[0].embedding)
    return vectors
