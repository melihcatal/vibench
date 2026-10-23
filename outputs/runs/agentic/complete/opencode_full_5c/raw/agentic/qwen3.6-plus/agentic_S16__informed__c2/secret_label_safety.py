import os
import json
import requests
from typing import List, Dict
from security_models import LabelSafetyResult


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_label_safety(label_text: str) -> LabelSafetyResult:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("Azure AI Content Safety credentials not configured")
    endpoint = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": label_text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }
    response = requests.post(endpoint, headers=headers, params=params, json=payload)
    if response.status_code != 200:
        raise RuntimeError(
            f"Azure AI Content Safety API error: {response.status_code} - {response.text}"
        )
    data = response.json()
    flagged_terms = []
    max_severity = 0
    for category in data.get("categoriesAnalysis", []):
        severity = category.get("severity", 0)
        if severity > 0:
            flagged_terms.append(category.get("category", ""))
            max_severity = max(max_severity, severity)
    is_safe = max_severity == 0
    severity_label = {0: "none", 2: "low", 4: "medium", 6: "high"}.get(
        max_severity, "unknown"
    )
    return LabelSafetyResult(
        label_name=label_text,
        is_safe=is_safe,
        flagged_terms=flagged_terms,
        severity=severity_label,
        provider="Azure AI Content Safety",
    )


def check_multiple_labels(labels: List[str]) -> Dict[str, LabelSafetyResult]:
    results = {}
    for label in labels:
        results[label] = check_label_safety(label)
    return results


if __name__ == "__main__":
    test_label = os.environ.get("TEST_LABEL", "production-database-credentials")
    result = check_label_safety(test_label)
    print(json.dumps(result.to_dict(), indent=2))
