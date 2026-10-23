from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class SpeechRecognitionResult:
    text: str
    is_final: bool
    language: Optional[str] = None
    offset_milliseconds: Optional[int] = None
    duration_milliseconds: Optional[int] = None
    sentiment_score: Optional[float] = None
    sentiment_magnitude: Optional[float] = None
    speaker_id: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = field(default_factory=dict)

def normalize_azure_speech_result(azure_event, is_final: bool) -> SpeechRecognitionResult:
    return SpeechRecognitionResult(
        text=azure_event.result.text,
        is_final=is_final,
        raw_response={
            "reason": str(azure_event.result.reason),
            "text": azure_event.result.text,
            "json": azure_event.result.json
        }
    )
