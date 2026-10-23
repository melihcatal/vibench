from __future__ import annotations

from typing import Iterable, List, Tuple

from google.cloud import speech_v1p1beta1 as speech

from speech_models import TranscriptBatch, TranscriptEvent, normalize_events


def partial_results(responses: Iterable[speech.StreamingRecognizeResponse]) -> TranscriptBatch:
    events: List[TranscriptEvent] = []
    for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue
            alt = result.alternatives[0]
            events.append(
                TranscriptEvent(
                    text=alt.transcript,
                    is_final=result.is_final,
                    confidence=getattr(alt, "confidence", None),
                    raw={"language_code": getattr(result, "language_code", None)},
                )
            )
    return normalize_events(events)
