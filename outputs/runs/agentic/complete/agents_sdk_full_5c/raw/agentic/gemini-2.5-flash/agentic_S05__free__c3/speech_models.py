from enum import Enum
from dataclasses import dataclass

class AudioEncoding(Enum):
    LINEAR16 = 1
    FLAC = 2
    MULAW = 3
    AMR = 4
    AMR_WB = 5
    OGG_OPUS = 6
    SPEEX_WITH_HEADER_BYTE = 7
    WEBM_OPUS = 8

@dataclass
class RecognitionConfig:
    encoding: AudioEncoding = AudioEncoding.LINEAR16
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = False

@dataclass
class StreamingRecognitionConfig:
    config: RecognitionConfig
    interim_results: bool = False

@dataclass
class InterimResultsConfig:
    interim_results: bool = False
