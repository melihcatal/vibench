import os
from typing import Dict
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def safety_threshold(text: str, thresholds: Dict[str, float] = None) -> Dict:
    if thresholds is None:
        thresholds = {"Hate": 0.7, "SelfHarm": 0.6, "Sexual": 0.8, "Violence": 0.7}

    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = {"text": text, "categories": list(thresholds.keys())}

    response = client.analyze_text(request)

    decision = "allow"
    violations = []
    category_scores = {}

    for category in response.categories_analysis:
        score = category.severity_score
        category_scores[category.category] = score

        threshold = thresholds.get(category.category, 0.7)
        if score >= threshold:
            decision = "block"
            violations.append(
                {"category": category.category, "score": score, "threshold": threshold}
            )

    return {
        "text": text,
        "decision": decision,
        "violations": violations,
        "category_scores": category_scores,
        "thresholds": thresholds,
    }
