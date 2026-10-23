from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CategoryScore:
    category: str
    severity: float  # 0.0 to 1.0


@dataclass
class SafetyResult:
    original_text: str
    category_scores: List[CategoryScore]
    blocked: bool
    rationale: str = ""
    redacted_text: Optional[str] = None
