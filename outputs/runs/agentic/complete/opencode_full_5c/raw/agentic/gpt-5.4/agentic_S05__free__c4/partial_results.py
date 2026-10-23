from __future__ import annotations

from typing import Any, Dict, List

from speech_models import StreamingTranscriptEvent, transcript_events_from_google


def collect_partial_results(response: Any) -> Dict[str, List[str]]:
    partials: List[str] = []
    finals: List[str] = []
    for event in transcript_events_from_google(response):
        if not event.text:
            continue
        if event.is_final:
            finals.append(event.text)
        else:
            partials.append(event.text)
    return {"partials": partials, "finals": finals}


def latest_display_text(event: StreamingTranscriptEvent) -> str:
    prefix = "FINAL" if event.is_final else "INTERIM"
    return f"{prefix}: {event.text}"
