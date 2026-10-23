
import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class TextSafetyRequest:
    """Represents a request for text content safety analysis."""
    text_content: str
    language_code: Optional[str] = "en"

@dataclasses.dataclass
class SafetyRating:
    """Represents a safety rating for a specific content category."""
    category: str
    probability: str
    is_supported: bool = True

@dataclasses.dataclass
class TextSafetyResponse:
    """Represents the response from a text content safety analysis."""
    blocked: bool
    safety_ratings: List[SafetyRating]

def normalize_text_content_safety_response(
    response_data: dict
) -> TextSafetyResponse:
    """Normalizes a raw content safety response into a standardized TextSafetyResponse.

    Args:
        response_data: A dictionary containing the raw response data.

    Returns:
        A TextSafetyResponse object.
    """
    blocked = response_data.get("blocked", False)
    safety_ratings_data = response_data.get("safety_ratings", [])
    
    safety_ratings = []
    for rating_data in safety_ratings_data:
        safety_ratings.append(
            SafetyRating(
                category=rating_data.get("category", "UNKNOWN"),
                probability=rating_data.get("probability", "UNKNOWN"),
                is_supported=rating_data.get("is_supported", True)
            )
        )
    
    return TextSafetyResponse(blocked=blocked, safety_ratings=safety_ratings)

