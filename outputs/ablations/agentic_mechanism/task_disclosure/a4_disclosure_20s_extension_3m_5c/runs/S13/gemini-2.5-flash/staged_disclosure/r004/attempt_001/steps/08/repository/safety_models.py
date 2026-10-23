
from typing import List, Dict, Any

class ContentSafetyRequest:
    """
    Represents a request for text content safety analysis.
    """
    def __init__(self, text_content: str):
        self.text_content = text_content

    def to_dict(self) -> Dict[str, Any]:
        return {"text_content": self.text_content}

class ContentSafetyResponse:
    """
    Represents a response from a text content safety analysis.
    """
    def __init__(self, categories: Dict[str, float], overall_score: float = 0.0):
        self.categories = categories
        self.overall_score = overall_score

    def to_dict(self) -> Dict[str, Any]:
        return {"categories": self.categories, "overall_score": self.overall_score}

def normalize_response(raw_response: Dict[str, Any]) -> ContentSafetyResponse:
    """
    Normalizes a raw content safety response into a standard ContentSafetyResponse object.
    This is a placeholder and would be adapted based on the specific third-party API response structure.
    """
    categories = raw_response.get("categories", {})
    overall_score = raw_response.get("overall_score", 0.0)
    return ContentSafetyResponse(categories=categories, overall_score=overall_score)
