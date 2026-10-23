
import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class ContentSafetyRequest:
    text_content: str
    client_id: Optional[str] = None
    session_id: Optional[str] = None

@dataclasses.dataclass
class CategoryScore:
    category: str
    score: float

@dataclasses.dataclass
class ContentSafetyResponse:
    id: str
    processed_content: str
    scores: List[CategoryScore]
    is_safe: bool

def normalize_text(text: str) -> str:
    """
    Normalizes text content for consistency before processing.
    Example: trimming whitespace, converting to lowercase.
    """
    return text.strip().lower()

