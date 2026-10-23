from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str = "en-US"
    enable_speaker_diarization: bool = False
    enable_word_time_offsets: bool = False


@dataclass
class WordInfo:
    word: str
    start_time: float
    end_time: float


@dataclass
class DiarizationSpeakerTag:
    speaker_tag: int
    words: List[WordInfo]


@dataclass
class TranscriptionResult:
    transcript: str
    word_timestamps: Optional[List[WordInfo]] = None
    diarized_segments: Optional[List[DiarizationSpeakerTag]] = None
