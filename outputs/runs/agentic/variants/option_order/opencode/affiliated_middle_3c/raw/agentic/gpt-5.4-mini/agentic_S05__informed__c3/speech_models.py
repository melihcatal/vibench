from dataclasses import dataclass
from typing import Optional


def normalize_text(text: Optional[str]) -> str:
    return " ".join((text or "").strip().split())


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    language: Optional[str] = None


@dataclass
class TranscribeRequest:
    language_code: str = "en-US"
    punctuation: bool = True
    sample_rate_hz: int = 16000
