from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from speech_models import TranscriptEvent


@dataclass(slots=True)
class PartialResultBuffer:
    partials: List[str] = field(default_factory=list)
    finals: List[str] = field(default_factory=list)

    def handle_event(self, event: TranscriptEvent) -> str:
        if event.is_final:
            self.finals.append(event.text)
            self.partials.clear()
            return event.text
        self.partials.append(event.text)
        return event.text

    def latest(self) -> str:
        return self.finals[-1] if self.finals else (self.partials[-1] if self.partials else "")


def handle_partial_and_final(event: dict) -> str:
    buffer = PartialResultBuffer()
    return buffer.handle_event(TranscriptEvent(text=event.get("text", ""), is_final=bool(event.get("is_final")), raw=event))
