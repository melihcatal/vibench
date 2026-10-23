from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Word:
    word: str
    start: float
    end: float
    confidence: float
    punctuated_word: Optional[str] = None

@dataclass
class Alternative:
    transcript: str
    confidence: float
    words: List[Word]

@dataclass
class Channel:
    alternatives: List[Alternative]

@dataclass
class StreamingTranscript:
    is_final: bool
    channel: Channel
    speech_final: bool
    start: float
    duration: float
