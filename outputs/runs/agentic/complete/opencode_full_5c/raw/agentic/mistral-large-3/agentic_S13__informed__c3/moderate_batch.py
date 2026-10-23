from typing import List
from safety_client import PerspectiveClient
from safety_models import BatchModerationResult, ModerationResponse, AttributeScore


def moderate_batch(texts: List[str]) -> BatchModerationResult:
    """Moderate a batch of user messages using Perspective API and return per-message decisions."""
    client = PerspectiveClient()
    results = []

    for text in texts:
        raw_response = client.moderate_text(text)
        attribute_scores = {}
        for attr, details in raw_response.get("attributeScores", {}).items():
            attribute_scores[attr] = AttributeScore(
                summary_score=details.get("summaryScore", {}).get("value", 0.0)
            )
        results.append(
            ModerationResponse(
                attribute_scores=attribute_scores, raw_response=raw_response
            )
        )

    return BatchModerationResult(results=results)
