import os
from speech_client import get_openai_client
from speech_models import SafetyResult


def check_script_safety(
    text: str,
    model: str = "text-moderation-latest",
) -> SafetyResult:
    client = get_openai_client()
    response = client.moderations.create(
        model=model,
        input=text,
    )
    result = response.results[0]
    flagged_categories = [
        category
        for category, flagged in result.categories.model_dump().items()
        if flagged
    ]
    details = {
        category: score
        for category, score in result.category_scores.model_dump().items()
        if score > 0
    }
    return SafetyResult(
        is_safe=not result.flagged,
        flagged_categories=flagged_categories,
        details=details,
    )
