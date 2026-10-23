import os
from typing import Dict, Any, Optional
from openai import OpenAI


def safety_threshold(
    text: str, thresholds: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text using OpenAI's moderation API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    default_thresholds = {
        "harassment": 0.8,
        "hate": 0.8,
        "self-harm": 0.7,
        "sexual": 0.8,
        "violence": 0.8,
        "harassment/threatening": 0.9,
        "hate/threatening": 0.9,
        "self-harm/intent": 0.6,
        "self-harm/instructions": 0.6,
        "sexual/minors": 0.7,
        "violence/graphic": 0.8,
    }

    if thresholds:
        default_thresholds.update(thresholds)

    client = OpenAI(api_key=api_key)

    response = client.moderations.create(model="text-moderation-latest", input=text)

    result = response.results[0]
    category_scores = result.category_scores.model_dump()

    decisions = {}
    allow = True

    for category, score in category_scores.items():
        threshold = default_thresholds.get(category, 0.8)
        is_flagged = score > threshold
        decisions[category] = {
            "score": score,
            "threshold": threshold,
            "flagged": is_flagged,
        }
        if is_flagged:
            allow = False

    return {
        "text": text,
        "allow": allow,
        "decisions": decisions,
        "overall_flagged": not allow,
    }
