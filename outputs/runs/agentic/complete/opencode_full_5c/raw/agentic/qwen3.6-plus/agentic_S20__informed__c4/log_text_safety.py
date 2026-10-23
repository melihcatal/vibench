import os

import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def build_safety_url():
    base = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    return (
        f"{base}/contentsafety/text:analyze"
        f"?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    )


def get_safety_headers():
    return {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }


def build_safety_payload(text, categories=None):
    default_categories = [
        "Hate",
        "SelfHarm",
        "Sexual",
        "Violence",
    ]
    return {
        "text": text,
        "categories": categories or default_categories,
        "outputType": "FourSeverityLevels",
    }


def analyze_text_safety(text, categories=None):
    url = build_safety_url()
    headers = get_safety_headers()
    payload = build_safety_payload(text, categories=categories)

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def check_log_message_safety(log_message, categories=None):
    result = analyze_text_safety(log_message, categories=categories)
    categories_result = result.get("categoriesAnalysis", [])
    has_unsafe = any(cat.get("severity", 0) > 0 for cat in categories_result)
    return {
        "text": log_message,
        "is_unsafe": has_unsafe,
        "category_results": categories_result,
        "raw_response": result,
    }


def log_text_safety(log_messages, categories=None):
    if isinstance(log_messages, str):
        log_messages = [log_messages]

    results = []
    for msg in log_messages:
        results.append(check_log_message_safety(msg, categories=categories))
    return results
