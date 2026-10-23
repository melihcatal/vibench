
import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class TextSafetyRequest:
    text_content: str
    
@dataclasses.dataclass
class SafetyRating:
    category: str
    probability: str

@dataclasses.dataclass
class TextSafetyResponse:
    ratings: List[SafetyRating]

def normalize_safety_response(response: Dict[str, Any]) -> TextSafetyResponse:
    # This is a placeholder for actual normalization logic
    # The exact structure of the upstream service's response would dictate this.
    ratings = []
    if "safetyRatings" in response:
        for rating_data in response["safetyRatings"]:
            ratings.append(SafetyRating(
                category=rating_data.get("category", "UNKNOWN"),
                probability=rating_data.get("probability", "UNKNOWN")
            ))
    return TextSafetyResponse(ratings=ratings)

def create_text_safety_request(text: str) -> TextSafetyRequest:
    return TextSafetyRequest(text_content=text)
