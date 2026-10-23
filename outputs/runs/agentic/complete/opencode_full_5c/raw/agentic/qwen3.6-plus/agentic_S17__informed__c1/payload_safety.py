import os
import requests
from typing import Dict, List, Optional


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_payload_safety(
    text: str,
    categories: Optional[List[str]] = None,
    threshold: float = 0.5,
) -> Dict:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )

    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    category_map = {
        "HATE": "Hate",
        "SELF_HARM": "SelfHarm",
        "SEXUAL": "Sexual",
        "VIOLENCE": "Violence",
    }

    if categories:
        analysis_categories = [category_map.get(c, c) for c in categories]
    else:
        analysis_categories = list(category_map.values())

    payload = {
        "text": text,
        "categories": analysis_categories,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, params=params, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    category_scores = {}
    flagged_categories = []
    for cat_result in result.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        normalized_score = severity / 7.0
        category_scores[cat_name] = normalized_score
        if normalized_score >= threshold:
            flagged_categories.append(cat_name)

    is_safe = len(flagged_categories) == 0

    return {
        "is_safe": is_safe,
        "category_scores": category_scores,
        "flagged_categories": flagged_categories,
        "request_id": response.headers.get("x-ms-request-id", ""),
    }


if __name__ == "__main__":
    sample_text = "This is a safe text payload for testing."
    result = check_payload_safety(sample_text)
    print(result)
