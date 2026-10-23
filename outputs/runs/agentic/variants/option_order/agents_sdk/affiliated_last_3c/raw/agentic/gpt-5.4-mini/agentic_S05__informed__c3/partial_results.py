from __future__ import annotations

from typing import Iterable, List

from speech_models import TranscriptEvent, normalize_text


class PartialResultAccumulator:
    def __init__(self) -> None:
        self.partial: str = ""
        self.final_segments: List[str] = []

    def update(self, event: TranscriptEvent) -> str:
        text = normalize_text(event.text)
        if event.is_final:
            if text:
                self.final_segments.append(text)
            self.partial = ""
        else:
            self.partial = text
        return self.current_text()

    def current_text(self) -> str:
        parts = [*self.final_segments]
        if self.partial:
            parts.append(self.partial)
        return normalize_text(" ".join(parts))


def handle_partial_and_final(events: Iterable[TranscriptEvent]) -> List[str]:
    acc = PartialResultAccumulator()
    outputs: List[str] = []
    for event in events:
        outputs.append(acc.update(event))
    return outputs
