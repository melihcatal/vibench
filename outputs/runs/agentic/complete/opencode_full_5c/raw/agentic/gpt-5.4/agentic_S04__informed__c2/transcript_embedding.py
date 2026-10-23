from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


def transcript_embedding(transcript_segments: Iterable[str]) -> List[List[float]]:
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=list(transcript_segments),
    )
    return [item.embedding for item in response.data]
