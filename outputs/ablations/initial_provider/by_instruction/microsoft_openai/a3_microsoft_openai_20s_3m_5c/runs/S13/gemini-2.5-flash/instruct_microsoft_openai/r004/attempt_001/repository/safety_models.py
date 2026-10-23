from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TextModerationRequest:
    text: str

@dataclass
class TextModerationResponse:
    categories: Optional[List[dict]] = None
    hate_category_score: Optional[float] = None
    self_harm_category_score: Optional[float] = None
    sexual_category_score: Optional[float] = None
    violence_category_score: Optional[float] = None
    block_id: Optional[str] = None
    block_lists_match_result: Optional[List[dict]] = None
    sentiment: Optional[int] = None
