from dataclasses import dataclass
from typing import List, Optional

@dataclass
class WordTimestamp:
    text: str
    start: int
    end: int
    confidence: float

@dataclass
class DiarizedUtterance:
    speaker: str
    text: str
    start: int
    end: int

@dataclass
class TranscriptionResult:
    job_id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[WordTimestamp]] = None
    utterances: Optional[List[DiarizedUtterance]] = None
