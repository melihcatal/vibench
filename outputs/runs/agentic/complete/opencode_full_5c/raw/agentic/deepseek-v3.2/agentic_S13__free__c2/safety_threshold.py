import os
from openai import OpenAI
from typing import Dict, Any


def safety_threshold(text: str, thresholds: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text using OpenAI's moderation API.
    """
    if thresholds is None:
        thresholds = {
            "hate": 0.8,
            "hate/threatening": 0.7,
            "harassment": 0.8,
            "harassment/threatening": 0.7,
            "self-harm": 0.9,
            "self-harm/intent": 0.8,
            "self-harm/instructions": 0.7,
            "sexual": 0.8,
            "sexual/minors": 0.6,
            "violence": 0.8,
            "violence/graphic": 0.7,
        }

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(model="text-moderation-latest", input=text)

    result = response.results[0]

    # Apply thresholds
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

    # Check each category against threshold
    violations = {}
    allowed = True

    for category, score in category_scores.items():
        threshold = thresholds.get(category, 0.8)  # Default threshold
        if score > threshold:
            violations[category] = {
                "score": score,
                "threshold": threshold,
                "exceeds": True,
            }
            allowed = False
        else:
            violations[category] = {
                "score": score,
                "threshold": threshold,
                "exceeds": False,
            }

    return {
        "allowed": allowed,
        "violations": violations,
        "category_scores": category_scores,
        "thresholds_applied": thresholds,
        "flagged_by_openai": result.flagged,
    }
