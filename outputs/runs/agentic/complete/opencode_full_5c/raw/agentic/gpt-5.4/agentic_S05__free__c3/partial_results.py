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


def latest_transcript_state(
    events: Iterable[StreamingTranscriptEvent],
) -> Dict[str, str]:
    latest_partial = ""
    committed: List[str] = []
    for event in events:
        if event.is_final:
            if event.text:
                committed.append(event.text)
            latest_partial = ""
        else:
            latest_partial = event.text
    return {
        "interim": latest_partial,
        "final": " ".join(
            segment.strip() for segment in committed if segment.strip()
        ).strip(),
    }
