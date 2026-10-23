"""Check secret labels and notes for unsafe text using Azure AI Content Safety."""

import os
import requests
from typing import Any


AZURE_CONTENT_SAFETY_ENDPOINT_DEFAULT = (
    "https://{resource}.cognitiveservices.azure.com"
)


def check_secret_label_safety(
    text: str,
    categories: list[str] | None = None,
    endpoint: str | None = None,
) -> dict[str, Any]:
    """Analyze secret labels and notes for unsafe content via Azure AI Content Safety.

    Args:
        text: The label or note text to analyze.
        categories: Content categories to check. Defaults to Hate, SelfHarm,
            Sexual, Violence.
        endpoint: Azure Content Safety endpoint URL. Falls back to
            AZURE_CONTENT_SAFETY_ENDPOINT env var.

    Returns:
        A dict with 'safe' (bool), 'categories' (dict of category -> severity),
        and 'raw_response' for the full API response.

    Raises:
        ValueError: If required credentials are missing.
        requests.HTTPError: If the API call fails.
    """
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    if not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required"
        )

    if not categories:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    payload = {
        "text": text,
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    result = resp.json()

    category_scores: dict[str, int] = {}
    for cat_result in result.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "unknown")
        severity = cat_result.get("severity", 0)
        category_scores[cat_name] = severity

    max_severity = max(category_scores.values()) if category_scores else 0
    is_safe = max_severity <= 2

    return {
        "safe": is_safe,
        "categories": category_scores,
        "max_severity": max_severity,
        "raw_response": result,
    }


if __name__ == "__main__":
    sample = "This secret was rotated due to a suspected compromise."
    result = check_secret_label_safety(sample)
    print(f"Safe: {result['safe']}")
    print(f"Categories: {result['categories']}")
