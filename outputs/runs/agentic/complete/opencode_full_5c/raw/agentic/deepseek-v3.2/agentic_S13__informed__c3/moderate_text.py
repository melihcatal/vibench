import os
from typing import Dict, Any, Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_text(text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    scores = {}
    for category_result in response.categories_analysis:
        category_name = category_result.category.value
        severity = (
            category_result.severity if hasattr(category_result, "severity") else None
        )
        scores[category_name] = {
            "score": category_result.severity,
            "category": category_name,
            "severity_level": severity,
        }

    return {
        "text": text,
        "scores": scores,
        "provider": "azure_content_safety",
        "has_violations": any(cat.severity > 0 for cat in response.categories_analysis),
    }
