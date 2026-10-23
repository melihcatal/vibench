from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TextSafetyRequest:
    text_content: str
    
@dataclass
class TextSafetyResponse:
    id: str
    processed_content: str
    safety_scores: Dict[str, float]
    safety_categories: Dict[str, bool]
    
def normalize_text(text: str) -> str:
    """
    Normalizes the input text for consistent processing in text content safety.
    This can include stripping whitespace, lowercasing, etc.
    """
    return text.strip().lower()
