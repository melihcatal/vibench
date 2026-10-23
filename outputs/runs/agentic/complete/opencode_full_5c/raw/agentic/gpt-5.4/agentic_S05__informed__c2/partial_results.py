from __future__ import annotations

from typing import Any, List

from deepgram import LiveTranscriptionEvents

from speech_models import TranscriptEvent, normalize_deepgram_result


class PartialTranscriptHandler:
    def __init__(self) -> None:
        self.partial_text = ""
        self.final_events: List[TranscriptEvent] = []

    def consume(self, result: Any) -> TranscriptEvent:
        event = normalize_deepgram_result(result)
        if event.is_final:
            self.final_events.append(event)
            self.partial_text = ""
        else:
            self.partial_text = event.text
        return event

    def attach(self, connection: Any) -> None:
        async def _on_transcript(_: Any, result: Any, **__: Any) -> None:
            self.consume(result)

        connection.on(LiveTranscriptionEvents.Transcript, _on_transcript)

    @property
    def final_text(self) -> str:
        return " ".join(event.text for event in self.final_events if event.text)
