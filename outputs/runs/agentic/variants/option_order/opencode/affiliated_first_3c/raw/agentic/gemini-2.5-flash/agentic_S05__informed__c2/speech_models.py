from dataclasses import dataclass


@dataclass
class StreamingRecognitionConfig:
    language_code: str
    enable_automatic_punctuation: bool = False


@dataclass
class TranscriptionResult:
    transcript: str
    is_final: bool
    confidence: float
