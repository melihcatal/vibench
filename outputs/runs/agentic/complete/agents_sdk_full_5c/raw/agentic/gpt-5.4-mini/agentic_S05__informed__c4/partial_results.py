from __future__ import annotations

from typing import Iterable, List

from speech_models import NormalizedTranscriptEvent, normalize_transcript_text


def handle_partial_and_final_events(events: Iterable[NormalizedTranscriptEvent]) -> List[str]:
    rendered: List[str] = []
    partial = ""
    for event in events:
        text = normalize_transcript_text(event.text)
        if not text:
            continue
        if event.is_final:
            if partial:
                rendered.append(partial)
                partial = ""
            rendered.append(text)
        else:
            partial = text
    if partial:
        rendered.append(partial)
    return rendered


def merge_partial_transcript(previous: str, current: NormalizedTranscriptEvent) -> str:
    current_text = normalize_transcript_text(current.text)
    if current.is_final:
        return normalize_transcript_text(f"{previous} {current_text}")
    return current_text or previous
