from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class SafetyScore:
    category: str
    probability: float

@dataclass
class ModerationDecision:
    input_text: str
    flagged: bool
    scores: Dict[str, float] = field(default_factory=dict)
    spans: List[Dict[str, Any]] = field(default_factory=list)
