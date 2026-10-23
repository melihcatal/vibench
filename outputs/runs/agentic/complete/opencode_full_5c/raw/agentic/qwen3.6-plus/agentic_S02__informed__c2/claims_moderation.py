import os
import requests
from typing import List, Dict, Any
from identity_models import ModerationResult


AZURE_CONTENT_SAFETY_ENDPOINT_DEFAULT = os.getenv(
    "AZURE_CONTENT_SAFETY_ENDPOINT", "https://default.cognitiveservices.azure.com/"
)


def moderate_claims_text(
    text: str,
    api_key: str | None = None,
    endpoint: str | None = None,
    api_version: str = "2024-02-15-preview",
) -> ModerationResult:
    if api_key is None:
        api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    if endpoint is None:
        endpoint = AZURE_CONTENT_SAFETY_ENDPOINT_DEFAULT

    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    endpoint = endpoint.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    categories = {}
    max_severity = 0
    flagged = False

    for category_result in data.get("categoriesAnalysis", []):
        category_name = category_result.get("category", "unknown")
        severity = category_result.get("severity", 0)
        categories[category_name] = severity
        if severity > max_severity:
            max_severity = severity
        if severity >= 4:
            flagged = True

    overall_score = max_severity / 7.0 if max_severity > 0 else 0.0
    is_safe = not flagged

    details_parts = []
    for cat, sev in categories.items():
        if sev > 0:
            details_parts.append(f"{cat}: severity {sev}")

    return ModerationResult(
        text=text,
        is_safe=is_safe,
        categories=categories,
        overall_score=overall_score,
        flagged=flagged,
        details="; ".join(details_parts)
        if details_parts
        else "No content safety concerns detected",
    )


def moderate_multiple_claims(
    texts: List[str],
    api_key: str | None = None,
    endpoint: str | None = None,
) -> List[ModerationResult]:
    results = []
    for text in texts:
        result = moderate_claims_text(text, api_key=api_key, endpoint=endpoint)
        results.append(result)
    return results


def batch_moderate_claims(
    texts: List[str],
    api_key: str | None = None,
    endpoint: str | None = None,
    api_version: str = "2024-02-15-preview",
) -> Dict[str, Any]:
    if api_key is None:
        api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    if endpoint is None:
        endpoint = AZURE_CONTENT_SAFETY_ENDPOINT_DEFAULT

    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    endpoint = endpoint.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    blocklists = [{"text": t} for t in texts]
    payload = {"blocklistText": blocklists}

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("blocklistsAnalysis", []):
        categories = {}
        max_severity = 0
        flagged = False
        for cat_result in item.get("categoriesAnalysis", []):
            cat_name = cat_result.get("category", "unknown")
            sev = cat_result.get("severity", 0)
            categories[cat_name] = sev
            if sev > max_severity:
                max_severity = sev
            if sev >= 4:
                flagged = True

        overall_score = max_severity / 7.0 if max_severity > 0 else 0.0
        results.append(
            ModerationResult(
                text=item.get("text", ""),
                is_safe=not flagged,
                categories=categories,
                overall_score=overall_score,
                flagged=flagged,
            )
        )

    return {
        "results": [r.to_dict() for r in results],
        "total_analyzed": len(results),
        "flagged_count": sum(1 for r in results if r.flagged),
        "provider": "azure_ai_content_safety",
    }


if __name__ == "__main__":
    sample_text = "This is a sample user claim that should be moderated for safety."
    result = moderate_claims_text(sample_text)
    print(f"Text safe: {result.is_safe}")
    print(f"Flagged: {result.flagged}")
    print(f"Provider: azure_ai_content_safety")
