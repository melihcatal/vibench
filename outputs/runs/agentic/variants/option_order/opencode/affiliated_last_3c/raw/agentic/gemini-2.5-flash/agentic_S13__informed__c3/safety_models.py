from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ContentSafetyCategory:
    category: str  # e.g., "Hate", "SelfHarm"
    severity: int  # 0-7


@dataclass
class ContentSafetyResult:
    categories_analysis: List[ContentSafetyCategory] = field(default_factory=list)
    block_lists_match: List[Dict] = field(
        default_factory=list
    )  # Simplified representation


@dataclass
class ModerationRequest:
    text: str


@dataclass
class ModerationResponse:
    results: Dict[str, int]
    original_text: str = ""
