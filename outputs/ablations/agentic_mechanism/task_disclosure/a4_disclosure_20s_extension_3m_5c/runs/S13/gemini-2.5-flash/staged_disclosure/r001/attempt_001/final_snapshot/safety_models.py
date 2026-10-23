
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ContentSafetyRequest:
    text_content: str
    language_code: str = "en"

@dataclass
class ContentSafetyAttribute:
    category: str
    score: float
    severity: int

@dataclass
class ContentSafetyResponse:
    processed_content: str
    safety_attributes: List[ContentSafetyAttribute] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

def normalize_safety_attributes(raw_safety_data: Dict[str, Any]) -> List[ContentSafetyAttribute]:
    """
    Normalizes raw safety data from a content safety API into a list of ContentSafetyAttribute.

    Args:
        raw_safety_data: A dictionary containing the raw response from a content safety API.

    Returns:
        A list of ContentSafetyAttribute objects.
    """
    normalized_attributes = []
    # Example of how to parse a hypothetical content safety API response structure.
    # This will vary greatly depending on the actual API.
    # For demonstration, let's assume raw_safety_data has a structure like:
    # {
    #     "safetyRatings": [
    #         {"category": "TOXICITY", "score": 0.9, "severity": 4},
    #         {"category": "SEXUAL", "score": 0.1, "severity": 0},
    #     ]
    # }
    if "safetyRatings" in raw_safety_data:
        for item in raw_safety_data["safetyRatings"]:
            try:
                attribute = ContentSafetyAttribute(
                    category=item.get("category", "UNKNOWN"),
                    score=float(item.get("score", 0.0)),
                    severity=int(item.get("severity", 0))
                )
                normalized_attributes.append(attribute)
            except (ValueError, TypeError):
                # Handle cases where score or severity might not be convertible
                pass
    return normalized_attributes
