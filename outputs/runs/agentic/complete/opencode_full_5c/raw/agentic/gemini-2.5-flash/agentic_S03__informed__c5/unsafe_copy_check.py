from translation_client import get_content_safety_client
from translation_models import UnsafeContentCheckRequest, UnsafeContentCheckResponse
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
import os


def check_unsafe_copy(request: UnsafeContentCheckRequest) -> UnsafeContentCheckResponse:
    client = get_content_safety_client()

    # The categories to check for unsafe content
    categories = [
        TextCategory.VIOLENCE,
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
    ]

    # Build the request to the Azure AI Content Safety service
    analyze_text_options = AnalyzeTextOptions(text=request.text, categories=categories)

    response = client.analyze_text(analyze_text_options)

    is_unsafe = False
    category_scores = {}

    for category in response.categories_analysis:
        category_scores[category.category.value] = {
            "severity": category.severity,  # 0-7 severity score
        }
        if category.severity > 0:  # A severity of 0 means no issues found.
            is_unsafe = True

    return UnsafeContentCheckResponse(is_unsafe=is_unsafe, categories=category_scores)
