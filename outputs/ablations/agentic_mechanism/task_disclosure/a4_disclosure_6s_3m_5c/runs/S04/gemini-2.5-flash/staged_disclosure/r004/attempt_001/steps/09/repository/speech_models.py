import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class RecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    max_alternatives: int = 1
    enable_word_time_offsets: bool = False
    model: Optional[str] = None
    use_enhanced: Optional[bool] = None

@dataclasses.dataclass
class AudioSource:
    uri: str # e.g., gs://cloud-samples-data/speech/brooklyn_bridge.flac

@dataclasses.dataclass
class SpeechRecognitionRequest:
    audio: AudioSource
    config: RecognitionConfig

@dataclasses.dataclass
class WordInfo:
    word: str
    start_time: str
    end_time: str
    speaker_tag: Optional[int] = None

@dataclasses.dataclass
class SpeechRecognitionAlternative:
    transcript: str
    confidence: Optional[float] = None
    words: Optional[List[WordInfo]] = None

@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative]
    channel_tag: Optional[int] = None

@dataclasses.dataclass
class SpeechRecognitionResponse:
    results: List[SpeechRecognitionResult]
    total_billed_time: Optional[str] = None

def normalize_transcript(transcript: str) -> str:
    """A placeholder for transcript normalization.
    Real-world normalization might include:
    - Punctuation removal
    - Lowercasing
    - Number word-to-digit conversion
    - Etc.
    """
    return transcript.lower().strip()
