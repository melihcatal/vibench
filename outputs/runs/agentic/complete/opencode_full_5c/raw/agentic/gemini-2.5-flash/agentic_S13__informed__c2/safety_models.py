from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ModerationCategory:
    category: str
    severity: int
    detected: bool = False


@dataclass
class ModerationResult:
    text: str
    categories: List[ModerationCategory]
    block_id: Optional[str] = None
    block_level: Optional[int] = None


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    categories_detected: List[str]
