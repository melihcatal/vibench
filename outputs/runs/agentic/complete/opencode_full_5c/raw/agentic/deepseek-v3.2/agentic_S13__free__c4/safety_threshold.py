import os
from typing import Dict, Any
import openai


def safety_threshold(text: str, thresholds: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text using OpenAI's moderation API.
    """
    if thresholds is None:
        thresholds = {
            "hate": 0.8,
            "harassment": 0.8,
            "sexual": 0.7,
            "violence": 0.9,
            "self_harm": 0.9,
        }

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(model="text-moderation-latest", input=text)

    result = response.results[0]

    decisions = {}
    allow = True
    violating_categories = []

    category_scores = {
        "hate": result.category_scores.hate,
        "hate_threatening": result.category_scores.hate_threatening,
        "harassment": result.category_scores.harassment,
        "harassment_threatening": result.category_scores.harassment_threatening,
        "self_harm": result.category_scores.self_harm,
        "self_harm_intent": result.category_scores.self_harm_intent,
        "self_harm_instructions": result.category_scores.self_harm_instructions,
        "sexual": result.category_scores.sexual,
        "sexual_minors": result.category_scores.sexual_minors,
        "violence": result.category_scores.violence,
        "violence_graphic": result.category_scores.violence_graphic,
    }

    for category, threshold in thresholds.items():
        score = category_scores.get(category, 0.0)
        decision = score <= threshold
        decisions[category] = {
            "score": score,
            "threshold": threshold,
            "allowed": decision,
        }

        if not decision:
            allow = False
            violating_categories.append(category)

    return {
        "text": text,
        "overall_decision": "allow" if allow else "block",
        "allow": allow,
        "decisions": decisions,
        "violating_categories": violating_categories,
        "max_violation_score": max(
            [category_scores.get(cat, 0.0) for cat in violating_categories]
        )
        if violating_categories
        else 0.0,
    }
