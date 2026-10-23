from typing import Dict, Optional
from safety_client import PerspectiveClient
from safety_models import ModerationResponse, AttributeScore


def moderate_text(text: str, language: Optional[str] = "en") -> ModerationResponse:
    """Score user text for unsafe or policy-violating content using Perspective API."""
    client = PerspectiveClient()
    raw_response = client.moderate_text(text)

    attribute_scores = {}
    for attr, details in raw_response.get("attributeScores", {}).items():
        attribute_scores[attr] = AttributeScore(
            summary_score=details.get("summaryScore", {}).get("value", 0.0)
        )

    return ModerationResponse(
        attribute_scores=attribute_scores, raw_response=raw_response
    )
