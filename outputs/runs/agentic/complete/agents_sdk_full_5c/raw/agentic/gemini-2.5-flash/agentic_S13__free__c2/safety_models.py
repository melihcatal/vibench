from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class ModerationResult:
    """
    Represents the standardized result of a text moderation operation.
    This structure is designed to be compatible with outputs from services
    like Azure Content Safety, which provide category-based severity scores.
    """
    is_safe: bool
    categories: Dict[str, int] = field(default_factory=dict)
    # Additional fields could be added here for more detailed results, e.g.,
    # flagged_spans: List[TextSpan] = field(default_factory=list)
    # raw_response: Dict[str, Any] = field(default_factory=dict)
