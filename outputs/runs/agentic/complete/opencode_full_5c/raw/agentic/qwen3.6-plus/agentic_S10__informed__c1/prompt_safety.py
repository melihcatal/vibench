import os
import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")


def check_prompt_safety(text: str) -> dict:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required"
        )

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    result = response.json()

    categories_analysis = result.get("categoriesAnalysis", [])
    hate_severity = 0
    self_harm_severity = 0
    sexual_severity = 0
    violence_severity = 0

    for cat in categories_analysis:
        category = cat.get("category", "")
        severity = cat.get("severity", 0)
        if category == "Hate":
            hate_severity = severity
        elif category == "SelfHarm":
            self_harm_severity = severity
        elif category == "Sexual":
            sexual_severity = severity
        elif category == "Violence":
            violence_severity = severity

    max_severity = max(
        hate_severity, self_harm_severity, sexual_severity, violence_severity
    )
    is_safe = max_severity <= 2

    return {
        "is_safe": is_safe,
        "max_severity": max_severity,
        "hate_severity": hate_severity,
        "self_harm_severity": self_harm_severity,
        "sexual_severity": sexual_severity,
        "violence_severity": violence_severity,
        "raw_response": result,
    }
