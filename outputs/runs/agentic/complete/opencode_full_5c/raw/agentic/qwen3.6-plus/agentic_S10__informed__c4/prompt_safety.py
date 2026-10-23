import os
import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
API_VERSION = "2024-02-15-preview"


def check_prompt_safety(text: str) -> dict:
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
    params = {"api-version": API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
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
    }
    response = requests.post(url, headers=headers, params=params, json=payload)
    response.raise_for_status()
    result = response.json()
    return result


def check_generated_text_safety(text: str) -> dict:
    return check_prompt_safety(text)


def is_text_safe(text: str, threshold: int = 2) -> bool:
    result = check_prompt_safety(text)
    for category_result in result.get("categoriesAnalysis", []):
        if category_result.get("severity", 0) >= threshold:
            return False
    return True


def get_safety_summary(text: str) -> dict:
    result = check_prompt_safety(text)
    summary = {"safe": True, "flags": []}
    for category_result in result.get("categoriesAnalysis", []):
        severity = category_result.get("severity", 0)
        if severity > 0:
            summary["safe"] = False
            summary["flags"].append(
                {
                    "category": category_result.get("category", ""),
                    "severity": severity,
                }
            )
    return summary
