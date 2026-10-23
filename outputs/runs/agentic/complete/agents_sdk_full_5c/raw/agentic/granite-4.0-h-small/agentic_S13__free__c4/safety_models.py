# safety_models.py
"""Define local request, response, and normalization helpers for Text Content Safety.
"""
from typing import List, Dict, Any

class SafetyRequest:
    """Encapsulate a request for moderation.
    Attributes:
        model (str): The safety model identifier (e.g., 'text-moderation-stable').
        input (List[str]): Texts to evaluate.
        category_thresholds (Dict[str, float], optional): Custom thresholds per category.
    """
    def __init__(self, model: str, input_: List[str], category_thresholds: Dict[str, float] | None = None):
        self.model = model
        self.input = input_
        self.category_thresholds = category_thresholds or {}

    def to_openai_dict(self) -> Dict[str, Any]:
        """Convert to the payload expected by safety_client.py."""
        payload = {
            "model": self.model,
            "input": self.input
        }
        if self.category_thresholds:
            payload["category_thresholds"] = self.category_thresholds
        return payload

class SafetyResponse:
    """Encapsulate a parsed moderation response.
    Attributes:
        flagged (bool): Whether any unsafe content was detected.
        flagged_categories (List[str]): List of categories that triggered.
        details (Dict[str, float]): Optional confidence scores per category.
    """
    def __init__(self, flagged: bool, flagged_categories: List[str], details: Dict[str, float] | None = None):
        self.flagged = flagged
        self.flagged_categories = flagged_categories
        self.details = details or {}

    @staticmethod
def from_openai_result(result: Dict[str, Any]) -> 'SafetyResponse':
        """Build a SafetyResponse from the raw OpenAI moderation result."""
        flagged = result.get("flagged", False)
        categories = result.get("flagged_categories", [])
        # For demonstration we assume confidence values are under result['details']
        details = result.get("details", {})
        return SafetyResponse(flagged, categories, details)
