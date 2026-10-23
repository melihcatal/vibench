from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class SafetyRating:
    """Represents a single safety rating for a specific category."""
    category: str
    severity: int # Can be a simple score or level depending on the provider

@dataclass
class ModerationResult:
    """A normalized response from a content safety provider."""
    flagged: bool
    categories: Dict[str, Any] = field(default_factory=dict)
    ratings: List[SafetyRating] = field(default_factory=list)
