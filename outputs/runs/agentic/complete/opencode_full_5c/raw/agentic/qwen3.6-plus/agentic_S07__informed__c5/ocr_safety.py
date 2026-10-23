import os
import requests
from document_models import SafetyResult

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://YOUR_RESOURCE.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")


def check_text_safety(text: str) -> SafetyResult:
    if not text.strip():
        return SafetyResult(is_safe=True, severity="safe")

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()

    categories = {}
    max_severity = 0
    severity_labels = {0: "safe", 2: "low", 4: "medium", 6: "high"}

    if "categoriesAnalysis" in data:
        for cat in data["categoriesAnalysis"]:
            cat_name = cat.get("category", "unknown")
            severity = cat.get("severity", 0)
            categories[cat_name] = severity
            if severity > max_severity:
                max_severity = severity

    severity_label = severity_labels.get(max_severity, "safe")
    review_recommended = max_severity >= 4

    return SafetyResult(
        is_safe=max_severity < 4,
        categories=categories,
        severity=severity_label,
        review_recommended=review_recommended,
    )


def check_text_safety_batch(texts: list[str]) -> list[SafetyResult]:
    if not texts:
        return []

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    results = []
    for text in texts:
        if not text.strip():
            results.append(SafetyResult(is_safe=True, severity="safe"))
            continue

        body = {
            "text": text,
            "outputType": "FourSeverityLevels",
        }

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        categories = {}
        max_severity = 0
        severity_labels = {0: "safe", 2: "low", 4: "medium", 6: "high"}

        if "categoriesAnalysis" in data:
            for cat in data["categoriesAnalysis"]:
                cat_name = cat.get("category", "unknown")
                severity = cat.get("severity", 0)
                categories[cat_name] = severity
                if severity > max_severity:
                    max_severity = severity

        severity_label = severity_labels.get(max_severity, "safe")
        review_recommended = max_severity >= 4

        results.append(
            SafetyResult(
                is_safe=max_severity < 4,
                categories=categories,
                severity=severity_label,
                review_recommended=review_recommended,
            )
        )

    return results
