from __future__ import annotations

from typing import Iterable, List

from speech_models import NormalizedTranscript, TranscriptEvent, normalize_transcript_event


def handle_partial_and_final_results(events: Iterable[TranscriptEvent]) -> List[NormalizedTranscript]:
    results: List[NormalizedTranscript] = []
    for event in events:
        normalized = normalize_transcript_event(event)
        results.append(normalized)
    return results
