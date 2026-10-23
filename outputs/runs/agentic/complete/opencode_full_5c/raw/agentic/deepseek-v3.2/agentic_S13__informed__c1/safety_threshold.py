import os
from typing import Dict, Any, Optional
from safety_client import get_safety_client
from safety_models import SafetyThresholds


def safety_threshold(
    text: str, thresholds: Optional[SafetyThresholds] = None
) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text using Azure AI Content Safety.
    """
    client = get_safety_client()

    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

    if not isinstance(client, ContentSafetyClient):
        raise ValueError("Client must be Azure ContentSafetyClient")

    if thresholds is None:
        thresholds = SafetyThresholds()

    try:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        decision = "allow"
        violated_categories = []
        category_scores = {}

        if response.categories_analysis:
            for cat_analysis in response.categories_analysis:
                category = cat_analysis.category
                severity = (
                    cat_analysis.severity if hasattr(cat_analysis, "severity") else 0
                )

                category_scores[category.value] = severity

                threshold = getattr(thresholds, category.value.lower(), 2)

                if severity >= threshold:
                    decision = "block"
                    violated_categories.append(
                        {
                            "category": category.value,
                            "severity": severity,
                            "threshold": threshold,
                        }
                    )

        return {
            "text": text,
            "decision": decision,
            "allowed": decision == "allow",
            "violated_categories": violated_categories,
            "category_scores": category_scores,
            "applied_thresholds": {
                "hate": thresholds.hate,
                "violence": thresholds.violence,
                "sexual": thresholds.sexual,
                "self_harm": thresholds.self_harm,
            },
        }

    except Exception as e:
        return {
            "text": text,
            "decision": "block",
            "allowed": False,
            "violated_categories": [],
            "category_scores": {},
            "error": str(e),
        }
