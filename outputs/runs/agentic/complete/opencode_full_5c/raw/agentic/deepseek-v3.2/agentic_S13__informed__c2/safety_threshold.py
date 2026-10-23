import os
from typing import Dict
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from safety_client import get_content_safety_client


def safety_threshold(text: str, thresholds: Dict[str, int] = None) -> Dict:
    """Applies category thresholds to decide whether to allow text."""
    if thresholds is None:
        thresholds = {"Hate": 2, "SelfHarm": 2, "Sexual": 2, "Violence": 2}

    client = get_content_safety_client()

    request = {"text": text, "categories": list(thresholds.keys())}

    try:
        response = client.analyze_text(request)

        decision = "allow"
        exceeded_thresholds = []
        category_scores = {}

        for category_analysis in response.categories_analysis:
            category = category_analysis.category
            severity = category_analysis.severity
            threshold = thresholds.get(category, 2)

            category_scores[category] = severity

            if severity >= threshold:
                decision = "block"
                exceeded_thresholds.append(
                    {"category": category, "score": severity, "threshold": threshold}
                )

        return {
            "text": text,
            "decision": decision,
            "exceeded_thresholds": exceeded_thresholds,
            "category_scores": category_scores,
            "thresholds_applied": thresholds,
        }
    except Exception as e:
        return {
            "text": text,
            "decision": "error",
            "error": str(e),
            "exceeded_thresholds": [],
            "category_scores": {},
            "thresholds_applied": thresholds,
        }
