from __future__ import annotations

from typing import Any

from speech_models import (
    TranscriptEvent,
    join_final_transcripts,
    normalize_google_streaming_response,
)


class PartialResultHandler:
    def __init__(self) -> None:
        self.interim_text = ""
        self.final_events: list[TranscriptEvent] = []

    def consume_google_response(self, response: Any) -> list[TranscriptEvent]:
        events = normalize_google_streaming_response(response)
        for event in events:
            if event.is_final:
                self.final_events.append(event)
                self.interim_text = ""
            else:
                self.interim_text = event.text
        return events

    def current_state(self) -> dict[str, Any]:
        return {
            "interim_text": self.interim_text,
            "final_text": join_final_transcripts(self.final_events),
            "final_count": len(self.final_events),
        }
