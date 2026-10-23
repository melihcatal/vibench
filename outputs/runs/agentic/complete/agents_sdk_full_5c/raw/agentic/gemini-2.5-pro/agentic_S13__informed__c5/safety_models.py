from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ModerationRequest:
    """
    Represents a single text message to be moderated.
    """
    text: str
    user_id: Optional[str] = None

@dataclass
class ModerationCategoryResult:
    """
    Holds the result for a single moderation category.
    """
    category: str
    severity: int
    flagged: bool

@dataclass
class ModerationResult:
    """
    Represents the overall moderation decision for a text.
    """
    flagged: bool
    categories: List[ModerationCategoryResult]
    raw_response: Optional[Dict[str, Any]] = field(default=None, repr=False)
