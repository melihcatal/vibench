import os
from typing import List, Dict, Any
from safety_client import get_safety_client


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    """
    Moderates a batch of user messages and returns per-message decisions using Azure AI Content Safety.
    """
    client = get_safety_client()

    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety.models import AnalyzeTextOptions

    if not isinstance(client, ContentSafetyClient):
        raise ValueError("Client must be Azure ContentSafetyClient")

    results = []

    for message in messages:
        try:
            request = AnalyzeTextOptions(text=message)
            response = client.analyze_text(request)

            decision = "allow"
            max_severity = 0
            categories = {}

            if response.categories_analysis:
                for cat_analysis in response.categories_analysis:
                    category = cat_analysis.category
                    severity = (
                        cat_analysis.severity
                        if hasattr(cat_analysis, "severity")
                        else 0
                    )

                    categories[category.value] = {
                        "severity": severity,
                        "flagged": severity >= 2,
                    }

                    if severity > max_severity:
                        max_severity = severity

                    if severity >= 2:  # Medium severity or higher
                        decision = "block"

            results.append(
                {
                    "message": message,
                    "decision": decision,
                    "severity": max_severity,
                    "categories": categories,
                    "safe": decision == "allow",
                }
            )

        except Exception as e:
            results.append(
                {
                    "message": message,
                    "decision": "block",
                    "severity": 4,
                    "categories": {},
                    "safe": False,
                    "error": str(e),
                }
            )

    return results
