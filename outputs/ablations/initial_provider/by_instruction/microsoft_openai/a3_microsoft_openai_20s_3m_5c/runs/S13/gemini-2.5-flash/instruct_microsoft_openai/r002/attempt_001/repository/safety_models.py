from typing import Literal, TypedDict, Optional

class ModerationCategoryResult(TypedDict):
    category: str
    severity: int

class ModerationResult(TypedDict):
    is_allowed: bool
    reasons: list[str]
    category_scores: Optional[dict[str, ModerationCategoryResult]]

class BatchModerationItem(TypedDict):
    text: str
    is_unsafe: bool
    details: Optional[dict]

class RedactionResult(TypedDict):
    original_text: str
    redacted_text: str
    was_redacted: bool
