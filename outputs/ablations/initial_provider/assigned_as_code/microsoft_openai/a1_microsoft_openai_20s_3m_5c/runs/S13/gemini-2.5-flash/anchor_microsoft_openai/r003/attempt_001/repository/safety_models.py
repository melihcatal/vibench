from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ModerationResult:
    text: str
    categories: Dict[str, float]
    is_unsafe: bool = False

@dataclass
class TextCategories:
    hate: float = 0.0
    sexual: float = 0.0
    violence: float = 0.0
    self_harm: float = 0.0
