from typing import Dict, List
from safety_client import get_openai_client
from safety_models import ModerationDecision


def apply_safety_thresholds(
    text: str, thresholds: Dict[str, float]
) -> ModerationDecision:
    """
    Applies category thresholds to decide whether to allow text, using OpenAI's moderation API.
    """
    client = get_openai_client()
    response = client.moderations.create(input=text)

    result = response.results[0]

    is_safe = True
    violations = []

    category_scores = result.category_scores.model_dump()

    for category, threshold in thresholds.items():
        # The dictionary from model_dump() uses the original field names
        # so we need to handle the aliases if present in thresholds keys
        api_category_name = category.replace("_", "/")
        score = category_scores.get(category, 0.0)

        if score > threshold:
            is_safe = False
            violations.append(api_category_name)

    return ModerationDecision(
        text=text, is_safe=is_safe, violations=violations, scores=category_scores
    )
