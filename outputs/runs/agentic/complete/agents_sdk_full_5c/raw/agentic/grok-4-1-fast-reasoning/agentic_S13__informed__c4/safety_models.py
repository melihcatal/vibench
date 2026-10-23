from dataclasses import dataclass
from typing import Dict, List, Optional, Any

@dataclass
class ModerationResult:
    input_text: str
    flagged: bool
    categories: Dict[str, Any]
    scores: Optional[Dict[str, float]] = None
    spans: Optional[List[Any]] = None

@dataclass
class BatchModerationResult:
    results: List[ModerationResult]