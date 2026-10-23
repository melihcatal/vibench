from __future__ import annotations

import os
from typing import Dict, List

from openai import OpenAI

from speech_models import TranscriptResult


def transcript_embedding(result: TranscriptResult) -> List[Dict[str, object]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    segments = result.utterances or result.segments
    inputs = [segment.text for segment in segments if segment.text]
    if not inputs:
        return []
    response = client.embeddings.create(model="text-embedding-3-large", input=inputs)
    embedded: List[Dict[str, object]] = []
    for segment, item in zip(
        [segment for segment in segments if segment.text], response.data
    ):
        embedded.append(
            {
                "text": segment.text,
                "start": segment.start,
                "end": segment.end,
                "speaker": segment.speaker,
                "embedding": item.embedding,
            }
        )
    return embedded
