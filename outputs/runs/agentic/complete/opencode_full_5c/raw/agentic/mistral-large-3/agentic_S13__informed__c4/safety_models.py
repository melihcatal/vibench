from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class ModerationResponse(BaseModel):
    is_flagged: bool
    categories: Dict[str, bool]
    scores: Dict[str, float]
    normalized_text: Optional[str] = None


class RedactionResponse(BaseModel):
    redacted_text: str
    spans_redacted: List[Dict[str, Union[int, int, str]]]
    categories: Dict[str, bool]


class BatchModerationResponse(BaseModel):
    results: List[ModerationResponse]


def normalize_moderation_response(response: Dict) -> ModerationResponse:
    """Normalize Tisane moderation response into a structured format."""
    return ModerationResponse(
        is_flagged=response.get("is_flagged", False),
        categories=response.get("categories", {}),
        scores=response.get("scores", {}),
        normalized_text=response.get("normalized_text"),
    )


def normalize_redaction_response(response: Dict) -> RedactionResponse:
    """Normalize Tisane redaction response into a structured format."""
    return RedactionResponse(
        redacted_text=response.get("redacted_text", ""),
        spans_redacted=response.get("spans_redacted", []),
        categories=response.get("categories", {}),
    )


def normalize_batch_response(responses: List[Dict]) -> BatchModerationResponse:
    """Normalize Tisane batch moderation responses into a structured format."""
    return BatchModerationResponse(
        results=[normalize_moderation_response(response) for response in responses]
    )
