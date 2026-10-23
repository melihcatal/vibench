from dataclasses import dataclass
from typing import Optional

from speech_models import StreamingTranscript, normalize_transcript


@dataclass
class PartialResultHandler:
    last_partial: str = ""
    last_final: str = ""

    def handle_event(self, event: dict) -> Optional[StreamingTranscript]:
        text = normalize_transcript(event.get("text", ""))
        if not text:
            return None
        is_final = bool(event.get("is_final") or event.get("final") or event.get("speech_final"))
        transcript = StreamingTranscript(
            text=text,
            is_final=is_final,
            language=event.get("language"),
            confidence=event.get("confidence"),
        )
        if is_final:
            self.last_final = text
        else:
            self.last_partial = text
        return transcript
