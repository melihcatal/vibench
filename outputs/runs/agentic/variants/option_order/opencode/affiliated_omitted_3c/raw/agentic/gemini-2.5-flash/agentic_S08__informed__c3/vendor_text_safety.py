from typing import Optional
from document_client import get_azure_content_safety_client
from document_models import ModerationResult
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_vendor_text_safety(text: str) -> ModerationResult:
    content_safety_client = get_azure_content_safety_client()

    # Example categories for moderation. Adjust as needed.
    categories = [
        TextCategory.VIOLENCE,
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
    ]

    request = AnalyzeTextOptions(text=text, categories=categories)
    response = content_safety_client.analyze_text(request)

    is_safe = True
    moderation_categories = {}

    for category_result in response.categories:  # type: ignore
        # If any category has a severity greater than 0, it's not safe.
        if category_result.severity and category_result.severity > 0:
            is_safe = False
        moderation_categories[category_result.category.value] = {
            "severity": category_result.severity,
            "detected": category_result.severity > 0
            if category_result.severity is not None
            else False,
        }

    return ModerationResult(
        is_safe=is_safe, categories=moderation_categories, text=text
    )
