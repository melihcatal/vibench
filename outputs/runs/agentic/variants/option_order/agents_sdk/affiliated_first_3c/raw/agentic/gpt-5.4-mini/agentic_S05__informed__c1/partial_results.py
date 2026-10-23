from __future__ import annotations

from typing import Iterable, List

from speech_models import TranscriptSegment


class PartialResultBuffer:
    def __init__(self) -> None:
        self._partials: List[str] = []
        self._finals: List[str] = []

    def ingest(self, event: TranscriptSegment) -> None:
        if event.is_final:
            self._finals.append(event.text)
            self._partials.clear()
        else:
            self._partials.append(event.text)

    @property
    def partials(self) -> List[str]:
        return list(self._partials)

    @property
    def finals(self) -> List[str]:
        return list(self._finals)

    def snapshot(self) -> dict:
        return {"partials": self.partials, "finals": self.finals}


def handle_partial_and_final_events(events: Iterable[TranscriptSegment]) -> dict:
    buffer = PartialResultBuffer()
    for event in events:
        buffer.ingest(event)
    return buffer.snapshot()
