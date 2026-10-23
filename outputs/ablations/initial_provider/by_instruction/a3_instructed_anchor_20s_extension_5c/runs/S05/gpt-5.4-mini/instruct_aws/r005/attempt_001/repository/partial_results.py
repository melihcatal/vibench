from typing import Iterable, List

from speech_models import TranscriptEvent, normalize_transcript_event


def partial_and_final_results(events: Iterable[dict]) -> List[TranscriptEvent]:
    normalized = []
    for event in events:
        item = normalize_transcript_event(event)
        if item.text:
            normalized.append(item)
    return normalized
