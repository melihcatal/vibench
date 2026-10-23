import dataclasses
from typing import Optional, List


@dataclasses.dataclass
class RecognitionResult:
    text: str
    is_final: bool


@dataclasses.dataclass
class SpeechRecognitionConfig:
    language: str = "en-US"
    enable_punctuation: bool = True
    profanity_filter: bool = False


@dataclasses.dataclass
class TranscriptionChunk:
    text: str
    offset: int
    duration: int
