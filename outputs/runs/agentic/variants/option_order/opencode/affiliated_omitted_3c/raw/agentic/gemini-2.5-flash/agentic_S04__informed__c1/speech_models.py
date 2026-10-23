from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TranscriptionRequest:
    audio_url: str
    speaker_labels: Optional[bool] = False
    word_timestamps: Optional[bool] = False


@dataclass
class Word:
    text: str
    start: int
    end: int
    confidence: float


@dataclass
class Utterance:
    speaker: str
    text: str
    start: int
    end: int
    words: List[Word]


@dataclass
class TranscriptionResult:
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[Word]] = None
    utterances: Optional[List[Utterance]] = None
