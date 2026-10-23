"""
Later-step: Check corpus text before embedding.
Provider: Azure AI Content Safety via REST API.
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
from typing import Any, Dict, List, Optional

import requests


def get_azure_content_safety_config() -> Dict[str, str]:
    """Retrieve Azure Content Safety configuration from environment."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )
    return {"endpoint": endpoint.rstrip("/"), "key": key}


def check_corpus_safety(
    texts: List[str],
    categories: Optional[List[str]] = None,
    threshold: int = 4,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Check corpus text for safety concerns using Azure AI Content Safety.

    Azure AI Content Safety detects hate, self-harm, sexual, and violence content.

    Args:
        texts: List of text strings to analyze.
        categories: Optional list of categories to check
                    (Hate, SelfHarm, Sexual, Violence).
        threshold: Severity threshold (0-7); lower is more sensitive.
        endpoint: Optional override for AZURE_CONTENT_SAFETY_ENDPOINT.
        api_key: Optional override for AZURE_CONTENT_SAFETY_KEY.

    Returns:
        List of result dicts with safety analysis per text.
    """
    cfg = get_azure_content_safety_config()
    base_url = endpoint or cfg["endpoint"]
    resolved_key = api_key or cfg["key"]

    url = f"{base_url}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": resolved_key,
        "Content-Type": "application/json",
    }

    results: List[Dict[str, Any]] = []

    for text in texts:
        body: Dict[str, Any] = {
            "text": text,
            "categoriesAnalysis": [
                {"category": c}
                for c in (categories or ["Hate", "SelfHarm", "Sexual", "Violence"])
            ],
        }

        response = requests.post(url, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        analysis = response.json()

        flagged = False
        flagged_categories: List[str] = []
        for cat_result in analysis.get("categoriesAnalysis", []):
            severity = cat_result.get("severity", 0)
            if severity >= threshold:
                flagged = True
                flagged_categories.append(
                    f"{cat_result.get('category', 'Unknown')}:{severity}"
                )

        results.append(
            {
                "text": text,
                "flagged": flagged,
                "flagged_categories": flagged_categories,
                "raw_analysis": analysis,
            }
        )

    return results


def filter_safe_texts(
    texts: List[str],
    **kwargs: Any,
) -> List[str]:
    """Return only texts that pass the safety check."""
    results = check_corpus_safety(texts, **kwargs)
    return [r["text"] for r in results if not r["flagged"]]


if __name__ == "__main__":
    sample = [
        "This is a normal sentence about technology.",
        "This text contains potentially harmful content that should be moderated.",
    ]
    # Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
    # results = check_corpus_safety(sample)
    # print(results)
    print("Configure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to run.")
