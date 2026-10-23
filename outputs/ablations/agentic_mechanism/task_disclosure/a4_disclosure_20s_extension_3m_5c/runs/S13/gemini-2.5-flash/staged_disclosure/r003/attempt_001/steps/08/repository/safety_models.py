
import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class SafetyRating:
    category: str
    probability: str # e.g., "HIGH", "MEDIUM", "LOW", "NEGLIGIBLE"
    blocked: bool = False

@dataclasses.dataclass
class ContentSafetyRequest:
    text_content: str
    client_ip: Optional[str] = None
    session_id: Optional[str] = None

@dataclasses.dataclass
class ContentSafetyResponse:
    processed_content: str
    safety_ratings: List[SafetyRating]
    is_safe: bool = True
    moderation_id: Optional[str] = None

def normalize_text_content(text: str) -> str:
    """
    Performs basic normalization on text content for safety processing.
    This can include lowercasing, stripping extra whitespace, etc.
    """
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")
    
    # Example normalization: lowercase and strip leading/trailing whitespace
    normalized_text = text.lower().strip()
    
    # Further normalization steps can be added here, e.g.,
    # - Removing punctuation
    # - Handling multiple spaces
    # - Decoding HTML entities
    
    return normalized_text

