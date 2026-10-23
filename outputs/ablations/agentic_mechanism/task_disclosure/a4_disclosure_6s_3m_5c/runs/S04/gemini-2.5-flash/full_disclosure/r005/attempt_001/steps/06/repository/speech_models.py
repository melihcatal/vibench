import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class RecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_word_time_offsets: bool = False
    enable_automatic_punctuation: bool = False
    model: str = "default"

@dataclasses.dataclass
class RecognitionAudio:
    uri: Optional[str] = None

@dataclasses.dataclass
class LongRunningRecognizeRequest:
    config: RecognitionConfig
    audio: RecognitionAudio

@dataclasses.dataclass
class WordInfo:
    start_time: str
    end_time: str
    word: str

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
class LongRunningRecognizeResponse:
    results: List[SpeechRecognitionResult]

def normalize_transcript(response: LongRunningRecognizeResponse) -> str:
    full_transcript = []
    for result in response.results:
        if result.alternatives:
            full_transcript.append(result.alternatives[0].transcript)
    return " ".join(full_transcript)
