
import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class RecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    model: str = "default"

@dataclasses.dataclass
class StreamingRecognitionConfig:
    config: RecognitionConfig = dataclasses.field(default_factory=RecognitionConfig)
    interim_results: bool = False

@dataclasses.dataclass
class StreamingRecognitionRequest:
    audio_content: Optional[bytes] = None
    streaming_config: Optional[StreamingRecognitionConfig] = None

@dataclasses.dataclass
class SpeechRecognitionAlternative:
    transcript: str
    confidence: float

@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative]
    is_final: bool

@dataclasses.dataclass
class StreamingRecognitionResponse:
    results: List[SpeechRecognitionResult]

def normalize_transcript(transcript: str) -> str:
    """A placeholder for transcript normalization.
    Could include lowercasing, removing punctuation, etc.
    """
    return transcript.lower().strip()
