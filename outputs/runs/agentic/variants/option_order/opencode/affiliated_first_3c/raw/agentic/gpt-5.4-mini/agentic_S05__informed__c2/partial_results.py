from typing import Iterable, List

from speech_models import TranscriptEvent, normalize_event


def partial_results(events: Iterable[object]) -> List[TranscriptEvent]:
    results: List[TranscriptEvent] = []
    for event in events:
        normalized = normalize_event(event)
        if normalized.text:
            results.append(
                TranscriptEvent(
                    text=normalized.text,
                    is_final=normalized.is_final,
                    confidence=normalized.confidence,
                    words=normalized.words,
                )
            )
    return results
