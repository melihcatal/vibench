from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from speech_models import TranscriptWord


def moderate_transcript(segments: Iterable[TranscriptWord]) -> List[bool]:
    client = OpenAI()
    results: List[bool] = []
    for segment in segments:
        moderation = client.moderations.create(model="omni-moderation-latest", input=segment.text)
        results.append(not bool(moderation.results[0].flagged))
    return results
