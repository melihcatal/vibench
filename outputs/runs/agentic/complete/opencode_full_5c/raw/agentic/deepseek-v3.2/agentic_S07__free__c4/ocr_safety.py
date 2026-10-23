import os
from typing import Dict, Any
from openai import OpenAI
from document_client import get_openai_client
from document_models import SafetyCheckResult


def ocr_safety(text: str) -> SafetyCheckResult:
    """
    Check extracted document text for unsafe content using OpenAI Moderation API.

    Args:
        text: Text to check for safety

    Returns:
        SafetyCheckResult containing safety assessment
    """
    client = get_openai_client()

    response = client.moderations.create(model="text-moderation-latest", input=text)

    moderation_result = response.results[0]
    categories = moderation_result.categories
    category_scores = moderation_result.category_scores

    category_dict = {}
    for category_name in categories.__dict__.keys():
        if not category_name.startswith("_"):
            category_value = getattr(categories, category_name)
            if category_value:
                score = getattr(category_scores, category_name, 0.0)
                category_dict[category_name] = float(score)

    is_safe = not moderation_result.flagged

    return SafetyCheckResult(
        text=text,
        is_safe=is_safe,
        categories=category_dict,
        provider="openai",
        model_id="text-moderation-latest",
        metadata={"flagged": moderation_result.flagged, "categories": category_dict},
    )
