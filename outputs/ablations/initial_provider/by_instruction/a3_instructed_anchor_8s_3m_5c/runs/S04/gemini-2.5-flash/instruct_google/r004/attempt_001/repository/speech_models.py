import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class TranscriptionConfig:
    audio_uri: str
    language_code: str = "en-US"
    enable_speaker_diarization: bool = False
    enable_word_time_offsets: bool = False

@dataclasses.dataclass
class TranscriptionJob:
    name: str
    status: str
    uri: Optional[str] = None

@dataclasses.dataclass
class WordInfo:
    start_time: str
    end_time: str
    word: str
    speaker_tag: Optional[int] = None

@dataclasses.dataclass
class TranscriptionAlternative:
    transcript: str
    confidence: float
    words: List[WordInfo]

@dataclasses.dataclass
class TranscriptionResult:
    alternatives: List[TranscriptionAlternative]
    result_end_time: str
    language_code: str
    channel_tag: Optional[int] = None
