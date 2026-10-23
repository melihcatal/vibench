import os
from openai import OpenAI
from typing import Dict, Any, Optional


def safety_threshold(
    text: str, thresholds: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Apply category thresholds to decide whether to allow text using OpenAI's moderation API.
    """
    if thresholds is None:
        thresholds = {
            "hate": 0.8,
            "hate/threatening": 0.8,
            "harassment": 0.8,
            "harassment/threatening": 0.8,
            "self-harm": 0.8,
            "self-harm/intent": 0.8,
            "self-harm/instructions": 0.8,
            "sexual": 0.8,
            "sexual/minors": 0.8,
            "violence": 0.8,
            "violence/graphic": 0.8,
        }

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(model="text-moderation-latest", input=text)

    result = response.results[0]

    category_scores = {
        "hate": result.category_scores.hate,
        "hate/threatening": result.category_scores.hate_threatening,
        "harassment": result.category_scores.harassment,
        "harassment/threatening": result.category_scores.harassment_threatening,
        "self-harm": result.category_scores.self_harm,
        "self-harm/intent": result.category_scores.self_harm_intent,
        "self-harm/instructions": result.category_scores.self_harm_instructions,
        "sexual": result.category_scores.sexual,
        "sexual/minors": result.category_scores.sexual_minors,
        "violence": result.category_scores.violence,
        "violence/graphic": result.category_scores.violence_graphic,
    }

    exceeded_thresholds = {}
    for category, score in category_scores.items():
        threshold = thresholds.get(category, 0.8)
        if score > threshold:
            exceeded_thresholds[category] = {
                "score": score,
                "threshold": threshold,
                "exceeded_by": score - threshold,
            }

    allow = len(exceeded_thresholds) == 0

    return {
        "allow": allow,
        "exceeded_thresholds": exceeded_thresholds,
        "category_scores": category_scores,
        "thresholds_applied": thresholds,
        "flagged": result.flagged,
    }
