from __future__ import annotations

from collections.abc import Iterable

from speech_models import TranscriptEvent
from speech_models import normalize_transcript_event


class PartialResultsHandler:
    def __init__(self) -> None:
        self._partials: list[str] = []
        self._finals: list[str] = []

    def handle(self, payload: object) -> TranscriptEvent:
        event = normalize_transcript_event(payload)
        if not event.text:
            return event
        if event.speech_final or event.utterance_final:
            self._finals.append(event.text)
            self._partials.clear()
        else:
            self._partials = [event.text]
        return event

    @property
    def interim_text(self) -> str:
        return " ".join(self._partials).strip()

    @property
    def final_text(self) -> str:
        return " ".join(self._finals).strip()

    def snapshot(self) -> dict[str, str]:
        return {"interim": self.interim_text, "final": self.final_text}


def iter_recognition_events(events: Iterable[object]) -> list[TranscriptEvent]:
    handler = PartialResultsHandler()
    return [handler.handle(event) for event in events]
