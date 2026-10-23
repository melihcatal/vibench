import os
from typing import Dict, Any, Optional
from safety_client import get_safety_client


def moderate_text(text: str) -> Dict[str, Any]:
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    client = get_safety_client()

    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

    if not isinstance(client, ContentSafetyClient):
        raise ValueError("Client must be Azure ContentSafetyClient")

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)

        result = {"text": text, "safe": True, "categories": {}, "severity": 0}

        if response.categories_analysis:
            max_severity = 0
            for cat_analysis in response.categories_analysis:
                category = cat_analysis.category
                severity = (
                    cat_analysis.severity if hasattr(cat_analysis, "severity") else 0
                )

                result["categories"][category.value] = {
                    "score": severity,
                    "severity": severity,
                }

                if severity > max_severity:
                    max_severity = severity
                    result["severity"] = severity

                if severity >= 2:  # Medium severity or higher
                    result["safe"] = False

        return result

    except Exception as e:
        return {
            "text": text,
            "safe": False,
            "error": str(e),
            "categories": {},
            "severity": 4,
        }
