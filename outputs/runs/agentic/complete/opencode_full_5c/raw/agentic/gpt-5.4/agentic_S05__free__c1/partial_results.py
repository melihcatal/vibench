from __future__ import annotations

from typing import Dict, Iterable, List

from speech_models import StreamingTranscriptEvent


def split_partial_and_final(
    events: Iterable[StreamingTranscriptEvent],
) -> Dict[str, List[StreamingTranscriptEvent]]:
    partial: List[StreamingTranscriptEvent] = []
    final: List[StreamingTranscriptEvent] = []
    for event in events:
        if event.is_final:
            final.append(event)
        else:
            partial.append(event)
    return {"partial": partial, "final": final}


def latest_interim_text(events: Iterable[StreamingTranscriptEvent]) -> str:
    latest = ""
    for event in events:
        if not event.is_final and event.text:
            latest = event.text
    return latest


def final_text(events: Iterable[StreamingTranscriptEvent]) -> str:
    return " ".join(
        event.text.strip() for event in events if event.is_final and event.text.strip()
    )
