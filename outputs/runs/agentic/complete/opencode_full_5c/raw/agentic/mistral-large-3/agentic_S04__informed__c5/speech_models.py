from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class TranscriptionRequest:
    audio_url: str
    enable_speaker_labels: bool = False
    enable_word_timestamps: bool = False


@dataclass
class TranscriptionResponse:
    transcription_id: str
    status: str
    transcript: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None
    utterances: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


@dataclass
class DiarizedUtterance:
    speaker: str
    text: str
    start: int
    end: int


@dataclass
class TimestampedWord:
    word: str
    start: int
    end: int
