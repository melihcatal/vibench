import os
from typing import Dict, Any
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_content_safety_client
from safety_models import (
    TextModerationRequest,
    TextModerationResponse,
    ModerationCategory,
)


def moderate_text(request: TextModerationRequest) -> TextModerationResponse:
    client = get_content_safety_client()

    categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
        TextCategory.SELF_HARM,
    ]

    request_body = AnalyzeTextOptions(text=request.text, categories=categories)
    response = client.analyze_text(request_body)

    categories_analysis: Dict[str, Any] = {}
    if response.categories_analysis:
        for category_analysis in response.categories_analysis:
            categories_analysis[category_analysis.category] = {
                "category": category_analysis.category,
                "severity": category_analysis.severity,
            }

    return TextModerationResponse(
        categories_analysis=[
            {
                "category": ModerationCategory.HATE.value,
                "score": categories_analysis.get(TextCategory.HATE, {}).get(
                    "severity", 0.0
                ),
            },
            {
                "category": ModerationCategory.SEXUAL.value,
                "score": categories_analysis.get(TextCategory.SEXUAL, {}).get(
                    "severity", 0.0
                ),
            },
            {
                "category": ModerationCategory.VIOLENCE.value,
                "score": categories_analysis.get(TextCategory.VIOLENCE, {}).get(
                    "severity", 0.0
                ),
            },
            {
                "category": ModerationCategory.SELF_HARM.value,
                "score": categories_analysis.get(TextCategory.SELF_HARM, {}).get(
                    "severity", 0.0
                ),
            },
        ],
    )
