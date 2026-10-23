from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class ModerationRequest(BaseModel):
    text: str
    categories: List[str]
    context: Dict[str, Any] = {}


class ModerationResponse(BaseModel):
    text: str
    is_safe: bool
    category_scores: Dict[str, int]
    block_reason: Optional[str] = None


class RedactionResponse(BaseModel):
    original_text: str
    redacted_text: str
    unsafe_spans: List[Dict[str, Any]]


def normalize_response(response: Dict[str, Any]) -> ModerationResponse:
    """
    Normalizes Azure AI Content Safety response into a standardized format.
    """
    category_scores = {
        result["category"]: result["severity"]
        for result in response.get("categoryScores", [])
    }

    is_safe = all(score <= 2 for score in category_scores.values())
    block_reason = None

    if not is_safe:
        block_reason = ", ".join(
            [category for category, score in category_scores.items() if score > 2]
        )

    return ModerationResponse(
        text=response.get("text", ""),
        is_safe=is_safe,
        category_scores=category_scores,
        block_reason=block_reason,
    )
