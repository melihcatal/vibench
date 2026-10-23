from __future__ import annotations

from typing import Iterable, List

from speech_models import TranscriptEvent, normalize_transcript


def handle_partial_and_final(events: Iterable[TranscriptEvent]) -> List[str]:
    emitted: List[str] = []
    current_partial = ""
    for event in events:
        text = normalize_transcript(event.transcript)
        if not text:
            continue
        if event.is_final:
            emitted.append(text)
            current_partial = ""
        else:
            current_partial = text
            emitted.append(f"PARTIAL: {current_partial}")
    return emitted
