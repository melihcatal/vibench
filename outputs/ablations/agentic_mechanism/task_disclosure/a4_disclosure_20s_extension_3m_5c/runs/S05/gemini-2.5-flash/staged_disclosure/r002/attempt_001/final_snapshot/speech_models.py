import dataclasses
from typing import Optional, List

@dataclasses.dataclass
class StreamingSpeechRecognitionRequest:
    audio_chunk: bytes
    encoding: str
    sample_rate_hertz: int
    language_code: str
    config: Optional[dict] = None

@dataclasses.dataclass
class SpeechRecognitionAlternative:
    transcript: str
    confidence: float

@dataclasses.dataclass
class StreamingSpeechRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative]
    is_final: bool

@dataclasses.dataclass
class StreamingSpeechRecognitionResponse:
    results: List[StreamingSpeechRecognitionResult]
    
def normalize_transcript(transcript: str) -> str:
    """
    Applies basic normalization to a speech-to-text transcript.
    """
    normalized_text = transcript.lower().strip()
    # Remove punctuation
    normalized_text = ''.join(char for char in normalized_text if char.isalnum() or char.isspace())
    return normalized_text
