from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ModerationCategory:
    category: str
    severity: int

@dataclass
class ModerationResult:
    text: str
    categories: List[ModerationCategory]
    is_flagged: bool

