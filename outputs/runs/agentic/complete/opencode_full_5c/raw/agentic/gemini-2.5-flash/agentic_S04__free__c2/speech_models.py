import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    enable_speaker_diarization: bool = False
    enable_word_time_offsets: bool = False


@dataclasses.dataclass
class WordInfo:
    word: str
    start_time: float
    end_time: float
    speaker_tag: Optional[int] = None


@dataclasses.dataclass
class Alternative:
    transcript: str
    confidence: float
    words: List[WordInfo]


@dataclasses.dataclass
class TranscriptionResult:
    alternatives: List[Alternative]
    language_code: str


@dataclasses.dataclass
class TranscriptionJob:
    operation_name: str
    status: str
    results: Optional[TranscriptionResult] = None
