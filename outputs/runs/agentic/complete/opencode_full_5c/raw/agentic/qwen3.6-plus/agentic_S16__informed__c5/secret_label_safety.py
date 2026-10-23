import os
import requests
from typing import Optional
from security_models import SafetyCheckResult


def check_secret_label_safety(
    label_text: str,
    endpoint: str = None,
    api_key: str = None,
    api_version: str = "2024-02-15-preview",
) -> SafetyCheckResult:
    endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    api_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    if not endpoint or not api_key:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )
    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version={api_version}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": label_text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "EightSeverityLevels",
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    categories = {}
    severity_scores = {}
    flagged_terms = []
    is_safe = True
    for category_result in data.get("categoriesAnalysis", []):
        cat = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        categories[cat] = severity
        severity_scores[cat] = severity
        if severity >= 4:
            is_safe = False
            flagged_terms.append(f"{cat}:{severity}")
    return SafetyCheckResult(
        text=label_text,
        is_safe=is_safe,
        categories=categories,
        severity_scores=severity_scores,
        flagged_terms=flagged_terms,
    )


def check_secret_labels_batch(
    labels: list,
    endpoint: str = None,
    api_key: str = None,
) -> list:
    results = []
    for label in labels:
        result = check_secret_label_safety(label, endpoint, api_key)
        results.append(result)
    return results


def validate_secret_metadata_safety(
    secret_id: str,
    metadata: dict,
    endpoint: str = None,
    api_key: str = None,
) -> dict:
    validation_results = {}
    for key, value in metadata.items():
        if isinstance(value, str) and value.strip():
            safety = check_secret_label_safety(value, endpoint, api_key)
            validation_results[key] = {
                "is_safe": safety.is_safe,
                "flagged": safety.flagged_terms,
            }
    return validation_results


if __name__ == "__main__":
    test_label = (
        "Production database credentials - do not share with unauthorized personnel"
    )
    result = check_secret_label_safety(test_label)
    print(f"Label: {result.text}")
    print(f"Safe: {result.is_safe}")
    print(f"Categories: {result.categories}")
