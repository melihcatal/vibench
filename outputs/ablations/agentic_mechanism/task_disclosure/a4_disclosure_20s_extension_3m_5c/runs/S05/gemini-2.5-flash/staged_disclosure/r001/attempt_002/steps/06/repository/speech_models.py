
from dataclasses import dataclass, field
from typing import List

@dataclass
class RecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    model: str = "default"
    profanity_filter: bool = False
    enable_word_time_offsets: bool = False

@dataclass
class StreamingRecognitionConfig:
    config: RecognitionConfig = field(default_factory=RecognitionConfig)
    interim_results: bool = False

@dataclass
class SpeechRecognitionAlternative:
    transcript: str
    confidence: float = 0.0

@dataclass
class StreamingRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative]
    is_final: bool

def normalize_transcript(transcript: str) -> str:
    """
    A simple normalization helper for the transcript.
    This can be extended for more complex normalization (e.g., punctuation, case).
    """
    return transcript.strip()

