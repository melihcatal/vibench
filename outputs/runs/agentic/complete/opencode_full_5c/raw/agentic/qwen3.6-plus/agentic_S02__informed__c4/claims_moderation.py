import os
import requests
from identity_models import ModerationResult


def moderate_claims_text(
    text: str,
    categories: list = None,
    endpoint: str = None,
    api_key: str = None,
) -> ModerationResult:
    api_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    if not api_key or not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )
    if not endpoint.startswith("http"):
        endpoint = f"https://{endpoint}.cognitiveservices.azure.com/"
    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    payload = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    result_data = response.json()
    category_scores = {}
    flagged = False
    for category_result in result_data.get("categoriesAnalysis", []):
        cat = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        category_scores[cat] = severity
        if severity >= 4:
            flagged = True
    is_safe = not flagged
    details = ""
    if flagged:
        flagged_cats = [cat for cat, sev in category_scores.items() if sev >= 4]
        details = f"Flagged categories: {', '.join(flagged_cats)}"
    return ModerationResult(
        text=text,
        is_safe=is_safe,
        categories=category_scores,
        confidence_scores={cat: sev / 7.0 for cat, sev in category_scores.items()},
        flagged=flagged,
        details=details,
    )


def moderate_multiple_claims(
    texts: list[str],
    categories: list = None,
) -> list[ModerationResult]:
    results = []
    for text in texts:
        result = moderate_claims_text(text, categories=categories)
        results.append(result)
    return results


def batch_moderate_claims(
    texts: list[str],
    categories: list = None,
) -> dict:
    moderation_results = moderate_multiple_claims(texts, categories=categories)
    total = len(moderation_results)
    flagged_count = sum(1 for r in moderation_results if r.flagged)
    safe_count = total - flagged_count
    return {
        "total_moderated": total,
        "safe_count": safe_count,
        "flagged_count": flagged_count,
        "results": [
            {
                "text": r.text,
                "is_safe": r.is_safe,
                "flagged": r.flagged,
                "categories": r.categories,
                "details": r.details,
            }
            for r in moderation_results
        ],
        "provider": "azure_content_safety",
        "endpoint": os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", ""),
    }
