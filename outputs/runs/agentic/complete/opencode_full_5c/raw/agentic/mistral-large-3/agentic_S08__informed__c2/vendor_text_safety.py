from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
import os
from typing import Dict, Any, List

# Provider-specific: Azure AI Content Safety
ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

client = ContentSafetyClient(ENDPOINT, AzureKeyCredential(KEY))


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    """
    Moderate vendor notes or memo fields using Azure AI Content Safety.
    """
    if not text:
        return {"is_safe": True, "categories": {}, "severity_scores": {}}

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    response = client.analyze_text(request)

    is_safe = all(score.severity <= 2 for score in response.categories_analysis)

    categories = {
        score.category.value: score.severity for score in response.categories_analysis
    }

    return {
        "is_safe": is_safe,
        "categories": categories,
        "severity_scores": {
            "hate": next(
                (
                    score.severity
                    for score in response.categories_analysis
                    if score.category == TextCategory.HATE
                ),
                0,
            ),
            "self_harm": next(
                (
                    score.severity
                    for score in response.categories_analysis
                    if score.category == TextCategory.SELF_HARM
                ),
                0,
            ),
            "sexual": next(
                (
                    score.severity
                    for score in response.categories_analysis
                    if score.category == TextCategory.SEXUAL
                ),
                0,
            ),
            "violence": next(
                (
                    score.severity
                    for score in response.categories_analysis
                    if score.category == TextCategory.VIOLENCE
                ),
                0,
            ),
        },
    }
