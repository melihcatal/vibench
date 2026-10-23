import os
from typing import Dict, Any, Optional
from safety_client import get_content_safety_client


def moderate_text(text: str, categories: Optional[list] = None) -> Dict[str, Any]:
    """
    Score user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    client = get_content_safety_client()

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

    category_map = {
        "Hate": TextCategory.HATE,
        "SelfHarm": TextCategory.SELF_HARM,
        "Sexual": TextCategory.SEXUAL,
        "Violence": TextCategory.VIOLENCE,
    }

    text_categories = [category_map[cat] for cat in categories if cat in category_map]

    request = AnalyzeTextOptions(text=text, categories=text_categories)

    response = client.analyze_text(request)

    result = {"text": text, "categories": {}, "overall_severity": 0}

    for category_result in response.categories_analysis:
        category_name = category_result.category.value
        severity = category_result.severity
        result["categories"][category_name] = {
            "severity": severity,
            "flagged": severity > 0,
        }
        if severity > result["overall_severity"]:
            result["overall_severity"] = severity

    return result
