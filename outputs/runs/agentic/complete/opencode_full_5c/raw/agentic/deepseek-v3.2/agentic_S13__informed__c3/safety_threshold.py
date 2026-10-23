import os
from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions


def safety_threshold(text: str, thresholds: Dict[str, int] = None) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    default_thresholds = {"Hate": 2, "SelfHarm": 2, "Sexual": 2, "Violence": 2}

    if thresholds:
        default_thresholds.update(thresholds)

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    category_decisions = {}
    for category_result in response.categories_analysis:
        category_name = category_result.category.value
        severity = category_result.severity
        threshold = default_thresholds.get(category_name, 2)

        category_decisions[category_name] = {
            "severity": severity,
            "threshold": threshold,
            "allowed": severity < threshold,
            "blocked": severity >= threshold,
        }

    overall_allowed = all(
        decision["allowed"] for decision in category_decisions.values()
    )

    return {
        "text": text,
        "category_decisions": category_decisions,
        "overall_decision": "ALLOW" if overall_allowed else "BLOCK",
        "provider": "azure_content_safety",
        "thresholds_applied": default_thresholds,
    }
