from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DiarizationConfig:
    enable_speaker_diarization: bool = True
    min_speaker_count: int = 1
    max_speaker_count: int = 6

@dataclass
class TranscriptionConfig:
    language_code: str = "en-US"
    sample_rate_hertz: int = 16000
    encoding: str = "LINEAR16"
    diarization_config: DiarizationConfig | None = None
    enable_word_time_offsets: bool = False

@dataclass
class WordInfo:
    word: str
    start_time: float # in seconds
    end_time: float   # in seconds

@dataclass
class TranscriptionResult:
    transcript: str
    words: Optional[List[WordInfo]] = None

@dataclass
class TranscriptionRequest:
    audio_uri: str
    config: TranscriptionConfig
