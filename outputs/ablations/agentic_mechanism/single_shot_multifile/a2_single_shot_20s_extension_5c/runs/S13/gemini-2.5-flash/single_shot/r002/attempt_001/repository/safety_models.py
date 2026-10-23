import dataclasses
from typing import List, Dict, Any, Optional

@dataclasses.dataclass
class ModerationCategory:
    category: str
    severity: int
    violates: bool

@dataclasses.dataclass
class ModerationResult:
    text: str
    categories: List[ModerationCategory]
    overall_decision: str
    redacted_text: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class BatchModerationInput:
    id: str
    text: str

@dataclasses.dataclass
class BatchModerationResult:
    id: str
    result: ModerationResult
