from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from speech_models import TranscriptWord


def transcript_embedding(segments: Iterable[TranscriptWord]) -> List[List[float]]:
    client = OpenAI()
    texts = [segment.text for segment in segments if segment.text]
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]
