from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class StreamingRecognitionEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    provider: str = "assemblyai"


def handle_partial_and_final_event(event: dict) -> StreamingRecognitionEvent:
    transcript = event.get("text") or event.get("transcript") or ""
    final = bool(event.get("is_final") or event.get("final") or event.get("message_type") == "FinalTranscript")
    confidence = event.get("confidence")
    if confidence is not None:
        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = None
    return StreamingRecognitionEvent(text=transcript, is_final=final, confidence=confidence)
