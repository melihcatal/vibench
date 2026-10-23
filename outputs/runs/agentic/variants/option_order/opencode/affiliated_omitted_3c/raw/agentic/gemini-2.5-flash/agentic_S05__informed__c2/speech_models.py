import dataclasses
import enum


@dataclasses.dataclass
class RecognitionConfig:
    sample_rate: int = 16000
    language: str = "en-US"
    punctuation: bool = True
    interim_results: bool = True


@dataclasses.dataclass
class RecognitionChunk:
    audio_data: bytes
    sequence_number: int


@dataclasses.dataclass
class TranscriptResult:
    text: str
    is_final: bool
    confidence: float
