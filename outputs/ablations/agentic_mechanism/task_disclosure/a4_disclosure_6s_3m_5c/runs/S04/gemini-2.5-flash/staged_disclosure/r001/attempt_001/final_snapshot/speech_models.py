
import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class RecognitionAudio:
    uri: str # URI of the audio file, e.g., gs://cloud-samples-data/speech/brooklyn_bridge.flac

@dataclasses.dataclass
class RecognitionConfig:
    encoding: str # Encoding of audio data, e.g., LINEAR16, FLAC, MULAW
    sample_rate_hertz: int # Sample rate in Hertz, e.g., 16000
    language_code: str # BCP-47 language tag, e.g., "en-US"
    enable_automatic_punctuation: Optional[bool] = False
    model: Optional[str] = "default" # Model to use, e.g., "default", "command_and_search", "phone_call"

@dataclasses.dataclass
class SpeechRecognitionRequest:
    audio: RecognitionAudio
    config: RecognitionConfig

@dataclasses.dataclass
class WordInfo:
    start_time: str
    end_time: str
    word: str
    confidence: float

@dataclasses.dataclass
class SpeechRecognitionAlternative:
    transcript: str
    confidence: float
    words: Optional[List[WordInfo]] = None

@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative]
    channel_tag: Optional[int] = None

@dataclasses.dataclass
class SpeechRecognitionResponse:
    results: List[SpeechRecognitionResult]
    total_billed_time: Optional[str] = None

def normalize_text(text: str) -> str:
    """
    Performs basic text normalization: lowercases the text and removes punctuation.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = ''.join(char for char in text if char.isalnum() or char.isspace())
    return text.strip()
