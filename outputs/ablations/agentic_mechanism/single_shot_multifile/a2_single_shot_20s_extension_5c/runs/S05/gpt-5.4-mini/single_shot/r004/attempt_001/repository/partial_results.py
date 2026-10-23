from typing import Any, Dict, Optional

from speech_models import TranscriptEvent, normalize_transcript_event


def handle_partial_and_final_events(event_payload: Dict[str, Any]) -> Optional[TranscriptEvent]:
    event = normalize_transcript_event(event_payload)
    if event is None:
        return None
    if event.is_final or event.confidence is not None:
        return event
    return event


class PartialTranscriptAccumulator:
    def __init__(self) -> None:
        self.partial_text = ""
        self.final_text = ""

    def ingest(self, event_payload: Dict[str, Any]) -> Optional[str]:
        event = normalize_transcript_event(event_payload)
        if event is None:
            return None
        if event.is_final:
            self.final_text = (self.final_text + " " + event.text).strip()
            self.partial_text = ""
            return self.final_text
        self.partial_text = event.text
        return self.partial_text

