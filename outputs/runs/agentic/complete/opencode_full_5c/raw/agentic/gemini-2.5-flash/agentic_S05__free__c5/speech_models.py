import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class StreamingRecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    interim_results: bool = True


@dataclasses.dataclass
class SpeechRecognitionResult:
    transcript: str
    is_final: bool
    confidence: float


@dataclasses.dataclass
class SpeechRecognitionResponse:
    results: List[SpeechRecognitionResult]
    end_of_stream: bool = False
