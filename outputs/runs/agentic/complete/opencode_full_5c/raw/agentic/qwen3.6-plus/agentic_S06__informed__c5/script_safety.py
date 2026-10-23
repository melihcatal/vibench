import os
import requests


def check_script_safety(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence",
        ],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def is_script_safe(text: str, max_severity: int = 2) -> bool:
    result = check_script_safety(text)
    categories = result.get("categoriesAnalysis", [])
    for category in categories:
        severity = category.get("severity", 0)
        if severity > max_severity:
            return False
    return True


def get_safety_categories(text: str) -> dict:
    result = check_script_safety(text)
    categories = {}
    for category in result.get("categoriesAnalysis", []):
        name = category.get("category", "unknown")
        severity = category.get("severity", 0)
        categories[name] = severity
    return categories
