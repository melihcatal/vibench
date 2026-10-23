import os
from typing import Dict, Any, Optional
from safety_client import get_content_safety_client
from safety_models import SafetyThresholds


def safety_threshold(
    text: str, thresholds: Optional[SafetyThresholds] = None
) -> Dict[str, Any]:
    """
    Apply category thresholds to decide whether to allow text using Azure AI Content Safety.
    """
    client = get_content_safety_client()

    if thresholds is None:
        thresholds = SafetyThresholds(hate=2, self_harm=2, sexual=2, violence=2)

    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

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

    decisions = {}
    allow = True

    for category_result in response.categories_analysis:
        category_name = category_result.category.value.lower()
        severity = category_result.severity

        threshold = getattr(thresholds, category_name, 2)

        flagged = severity >= threshold
        decisions[category_name] = {
            "severity": severity,
            "threshold": threshold,
            "flagged": flagged,
            "decision": "block" if flagged else "allow",
        }

        if flagged:
            allow = False

    return {
        "text": text,
        "allow": allow,
        "decisions": decisions,
        "overall_decision": "allow" if allow else "block",
    }
