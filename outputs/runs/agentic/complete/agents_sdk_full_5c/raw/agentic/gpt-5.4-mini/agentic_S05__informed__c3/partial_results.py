from __future__ import annotations

from typing import Iterable, List

from speech_models import StreamingTranscriptEvent, StreamingTranscriptResult


class PartialResultsBuffer:
    def __init__(self) -> None:
        self._events: List[StreamingTranscriptEvent] = []

    def handle_event(self, event: StreamingTranscriptEvent) -> None:
        self._events.append(event)

    def current(self) -> StreamingTranscriptResult:
        return StreamingTranscriptResult(events=list(self._events))

    def final_text(self) -> str:
        return " ".join(event.text for event in self._events if event.is_final and event.text).strip()

    def interim_text(self) -> str:
        return " ".join(event.text for event in self._events if not event.is_final and event.text).strip()


def merge_events(events: Iterable[StreamingTranscriptEvent]) -> StreamingTranscriptResult:
    return StreamingTranscriptResult(events=list(events))
