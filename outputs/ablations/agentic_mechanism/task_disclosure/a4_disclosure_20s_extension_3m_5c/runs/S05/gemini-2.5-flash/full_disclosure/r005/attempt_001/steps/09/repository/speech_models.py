
import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class RecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    max_alternatives: int = 1
    enable_automatic_punctuation: bool = False

@dataclasses.dataclass
class StreamingRecognitionConfig:
    config: RecognitionConfig = dataclasses.field(default_factory=RecognitionConfig)
    interim_results: bool = True

@dataclasses.dataclass
class StreamingRecognizeRequest:
    audio_content: Optional[bytes] = None
    streaming_config: Optional[StreamingRecognitionConfig] = None

@dataclasses.dataclass
class SpeechRecognitionAlternative:
    transcript: str
    confidence: float = 0.0

@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative]
    is_final: bool

@dataclasses.dataclass
class StreamingRecognizeResponse:
    results: List[SpeechRecognitionResult]
    end_of_stream: bool = False

def normalize_transcript(transcript: str) -> str:
    """Normalizes the transcript text."""
    # Example normalization: convert to lowercase and remove extra spaces
    return " ".join(transcript.lower().split())
