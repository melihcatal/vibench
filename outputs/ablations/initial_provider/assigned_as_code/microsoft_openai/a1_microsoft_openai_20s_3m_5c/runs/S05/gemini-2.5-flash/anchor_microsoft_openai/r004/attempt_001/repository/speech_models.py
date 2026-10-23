import dataclasses
from typing import Optional, List, Dict, Any

@dataclasses.dataclass
class AudioConfig:
    sample_rate_hz: int
    bits_per_sample: int
    channels: int

@dataclasses.dataclass
class SpeechRecognitionResult:
    text: str
    is_final: bool
    language_code: Optional[str] = None
    confidence: Optional[float] = None

@dataclasses.dataclass
class StreamingRecognitionConfig:
    language_code: str
    sample_rate_hz: int
    enable_automatic_punctuation: bool = False
    
def normalize_azure_result(azure_event: Dict[str, Any]) -> SpeechRecognitionResult:
    return SpeechRecognitionResult(
        text=azure_event["text"],
        is_final=azure_event["is_final"]
    )
