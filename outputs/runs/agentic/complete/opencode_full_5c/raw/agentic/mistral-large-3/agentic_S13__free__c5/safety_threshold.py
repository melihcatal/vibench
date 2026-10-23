from typing import Dict, Any
from moderate_text import moderate_text


def safety_threshold(text: str, thresholds: Dict[str, float]) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text using Google Cloud's Content Moderation API.
    """
    response = moderate_text(text)
    attribute_scores = response.get("attributeScores", {})

    decision = {"allow": True, "violations": []}

    for category, threshold in thresholds.items():
        score = (
            attribute_scores.get(category, {}).get("summaryScore", {}).get("value", 0.0)
        )
        if score >= threshold:
            decision["allow"] = False
            decision["violations"].append(
                {
                    "category": category,
                    "score": score,
                    "threshold": threshold,
                }
            )

    return decision
