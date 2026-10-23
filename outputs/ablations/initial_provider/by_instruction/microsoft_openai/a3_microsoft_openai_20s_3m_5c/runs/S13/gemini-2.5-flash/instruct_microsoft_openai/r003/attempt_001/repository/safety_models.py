from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class ModerationRequest:
    text: str

@dataclass
class ModerationResponse:
    id: str
    model: str
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    flagged: bool
