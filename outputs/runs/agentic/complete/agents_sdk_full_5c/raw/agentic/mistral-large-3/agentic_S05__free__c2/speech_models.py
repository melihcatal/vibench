from dataclasses import dataclass
from typing import Optional

@dataclass
class PartialResult:
    transcript: str

@dataclass
class FinalResult:
    transcript: str
    confidence: float

def normalize_transcript(text: str) -> str:
    return text.strip()