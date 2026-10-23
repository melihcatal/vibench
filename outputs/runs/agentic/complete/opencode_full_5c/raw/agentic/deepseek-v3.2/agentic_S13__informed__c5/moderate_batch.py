import os
from typing import List, Dict, Any
from safety_client import get_content_safety_client


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    """
    Moderate a batch of user messages and return per-message decisions using Azure AI Content Safety.
    """
    client = get_content_safety_client()

    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

    results = []

    for message in messages:
        request = AnalyzeTextOptions(
            text=message,
            categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE,
            ],
        )

        response = client.analyze_text(request)

        decision = "allow"
        category_decisions = {}

        for category_result in response.categories_analysis:
            category_name = category_result.category.value
            severity = category_result.severity
            flagged = severity > 0
            category_decisions[category_name] = {
                "flagged": flagged,
                "severity": severity,
            }
            if flagged:
                decision = "block"

        results.append(
            {
                "message": message,
                "decision": decision,
                "category_decisions": category_decisions,
                "overall_severity": max(
                    [cat["severity"] for cat in category_decisions.values()]
                ),
            }
        )

    return results
