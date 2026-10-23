import os
from typing import List, Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    results = []
    for message in messages:
        request = AnalyzeTextOptions(text=message)
        response = client.analyze_text(request)

        decisions = {}
        for category_result in response.categories_analysis:
            category_name = category_result.category.value
            severity = category_result.severity
            decisions[category_name] = {
                "decision": "BLOCK" if severity > 0 else "ALLOW",
                "severity": severity,
                "threshold_exceeded": severity > 0,
            }

        overall_decision = (
            "BLOCK"
            if any(cat.severity > 0 for cat in response.categories_analysis)
            else "ALLOW"
        )

        results.append(
            {
                "text": message,
                "decisions": decisions,
                "overall_decision": overall_decision,
                "provider": "azure_content_safety",
            }
        )

    return results
