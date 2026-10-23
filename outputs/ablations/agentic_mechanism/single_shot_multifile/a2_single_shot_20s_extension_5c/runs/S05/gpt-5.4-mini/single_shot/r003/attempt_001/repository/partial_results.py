from dataclasses import dataclass
from typing import Any, Dict, Optional

from speech_models import TranscriptEvent, normalize_transcript_event


@dataclass
class PartialResultsHandler:
    last_partial: Optional[str] = None
    final_text: str = ""

    def handle_event(self, event: Dict[str, Any]) -> TranscriptEvent:
        transcript_event = normalize_transcript_event(event)
        if transcript_event.is_final:
            if transcript_event.text:
                self.final_text = (self.final_text + " " + transcript_event.text).strip()
            self.last_partial = None
        else:
            self.last_partial = transcript_event.text
        return transcript_event

    def current_text(self) -> str:
        return (self.final_text + " " + (self.last_partial or "")).strip()
