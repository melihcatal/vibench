import dataclasses
from typing import List

# Based on Google Cloud Speech-to-Text API v1

@dataclasses.dataclass
class RecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    max_alternatives: int = 1
    profanity_filter: bool = False
    enable_word_time_offsets: bool = False
    enable_automatic_punctuation: bool = False

@dataclasses.dataclass
class StreamingRecognitionConfig:
    config: RecognitionConfig = dataclasses.field(default_factory=RecognitionConfig)
    single_utterance: bool = False
    interim_results: bool = False

@dataclasses.dataclass
class StreamingRecognizeRequest:
    audio_content: bytes = b''
    streaming_config: StreamingRecognitionConfig = dataclasses.field(default_factory=StreamingRecognitionConfig)

@dataclasses.dataclass
class WordInfo:
    start_time: float
    end_time: float
    word: str
    confidence: float

@dataclasses.dataclass
class SpeechRecognitionAlternative:
    transcript: str
    confidence: float
    words: List[WordInfo] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative] = dataclasses.field(default_factory=list)
    is_final: bool = False
    stability: float = 0.0

@dataclasses.dataclass
class StreamingRecognizeResponse:
    results: List[SpeechRecognitionResult] = dataclasses.field(default_factory=list)
    speech_event_type: str = ""

def normalize_transcript(response: StreamingRecognizeResponse) -> str:
    """Normalizes the transcript from a StreamingRecognizeResponse."""
    if not response.results:
        return ""
    
    # Get the most confident alternative from the first final result
    for result in response.results:
        if result.is_final and result.alternatives:
            return result.alternatives[0].transcript
    
    # If no final result, return the transcript from the first alternative of the first result
    if response.results[0].alternatives:
        return response.results[0].alternatives[0].transcript
    
    return ""
