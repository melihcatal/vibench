import dataclasses
from typing import Optional, Dict, Any

@dataclasses.dataclass
class SpeechConfig:
    api_key: str
    region: str
    language_code: Optional[str] = None
    sample_rate_hz: Optional[int] = None
    enable_automatic_punctuation: Optional[bool] = None

@dataclasses.dataclass
class SpeechResult:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    language: Optional[str] = None

def normalize_azure_speech_event(event: Any) -> SpeechResult:
    if hasattr(event.result, 'text'):
        return SpeechResult(
            text=event.result.text,
            is_final=event.result.reason == event.result.reason.RecognizedSpeech,
            confidence=getattr(event.result, 'confidence', None),
            language=getattr(event.result, 'language', None)
        )
    return SpeechResult(text="", is_final=False)
