from typing import Optional
from dataclasses import dataclass


@dataclass
class StreamingTranscript:
    text: str
    is_final: bool
    confidence: float
    words: Optional[list] = None
