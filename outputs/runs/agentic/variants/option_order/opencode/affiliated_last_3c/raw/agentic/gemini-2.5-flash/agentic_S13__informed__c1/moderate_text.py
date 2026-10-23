from safety_client import PerspectiveAPIClient
from safety_models import ModerationScore, ModerationResult
from typing import List


def moderate_text(text: str) -> ModerationResult:
    client = PerspectiveAPIClient()
    response = client.analyze(text)

    scores: List[ModerationScore] = []
    is_unsafe = False
    unsafe_attributes = []

    for attribute, data in response.get("attributeScores", {}).items():
        score = data["summaryScore"]["value"]
        scores.append(ModerationScore(attribute=attribute, score=score))
        # Simple rule: if any score is > 0.8, consider it unsafe for demonstration
        if score > 0.8:
            is_unsafe = True
            unsafe_attributes.append(attribute)

    return ModerationResult(
        text=text,
        scores=scores,
        is_unsafe=is_unsafe,
        unsafe_attributes=" ".join(unsafe_attributes),
    )
