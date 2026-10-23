"""Check corpus text before embedding using Azure AI Content Safety API.

Uses Azure AI Content Safety to analyze text for harmful content including hate,
self-harm, sexual, and violence categories before embedding is performed.
"""

import os
from typing import List, Dict, Any, Optional

import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

SAFETY_API_VERSION = "2024-02-15-preview"

SAFETY_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]


def build_safety_url(endpoint: str = None) -> str:
    """Build the Azure AI Content Safety analyze text URL.

    Args:
        endpoint: Azure Content Safety endpoint (falls back to env var).

    Returns:
        Full URL for the analyze text API.
    """
    ep = endpoint or AZURE_CONTENT_SAFETY_ENDPOINT
    if not ep:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required")
    ep = ep.rstrip("/")
    return f"{ep}/contentsafety/text:analyze?api-version={SAFETY_API_VERSION}"


def check_text_safety(
    text: str,
    endpoint: str = None,
    api_key: str = None,
    block_threshold: int = 4,
) -> Dict[str, Any]:
    """Check a single text string for safety violations via Azure AI Content Safety.

    Args:
        text: Text content to analyze.
        endpoint: Azure Content Safety endpoint.
        api_key: Azure Content Safety API key.
        block_threshold: Severity threshold (0-7); scores at or above block the text.

    Returns:
        Dict with 'safe' (bool), 'categories' (list of flagged categories),
        'details' (per-category severity scores), and 'blocked_reason'.
    """
    key = api_key or AZURE_CONTENT_SAFETY_KEY
    if not key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    url = build_safety_url(endpoint)

    payload = {
        "text": text,
        "categories": SAFETY_CATEGORIES,
        "outputType": "FourSeverityLevels",
    }

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": key,
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()
    categories_analysis = result.get("categoriesAnalysis", [])

    blocked_reasons = []
    category_scores = {}
    for cat_analysis in categories_analysis:
        cat_name = cat_analysis.get("category", "Unknown")
        severity = cat_analysis.get("severity", 0)
        category_scores[cat_name] = severity
        if severity >= block_threshold:
            blocked_reasons.append(f"{cat_name} (severity={severity})")

    return {
        "safe": len(blocked_reasons) == 0,
        "categories": blocked_reasons,
        "details": category_scores,
        "blocked_reason": "; ".join(blocked_reasons) if blocked_reasons else None,
    }


def check_corpus_safety(
    texts: List[str],
    endpoint: str = None,
    api_key: str = None,
    block_threshold: int = 4,
) -> Dict[str, Any]:
    """Check all texts in a corpus for safety before embedding.

    Args:
        texts: List of text strings to screen.
        endpoint: Azure Content Safety endpoint.
        api_key: Azure Content Safety API key.
        block_threshold: Severity threshold for blocking.

    Returns:
        Dict with 'total', 'safe_count', 'blocked_count', 'blocked_texts' (indices),
        and 'results' (per-text safety check results).
    """
    results = []
    blocked_indices = []
    safe_count = 0

    for i, text in enumerate(texts):
        check_result = check_text_safety(
            text,
            endpoint=endpoint,
            api_key=api_key,
            block_threshold=block_threshold,
        )
        results.append(check_result)
        if check_result["safe"]:
            safe_count += 1
        else:
            blocked_indices.append(i)

    return {
        "total": len(texts),
        "safe_count": safe_count,
        "blocked_count": len(blocked_indices),
        "blocked_indices": blocked_indices,
        "results": results,
    }


def filter_safe_texts(
    texts: List[str],
    endpoint: str = None,
    api_key: str = None,
    block_threshold: int = 4,
) -> List[str]:
    """Return only the texts that pass safety checks.

    Args:
        texts: List of texts to filter.
        endpoint: Azure Content Safety endpoint.
        api_key: Azure Content Safety API key.
        block_threshold: Severity threshold.

    Returns:
        Filtered list containing only safe texts.
    """
    corpus_result = check_corpus_safety(
        texts,
        endpoint=endpoint,
        api_key=api_key,
        block_threshold=block_threshold,
    )
    safe_texts = [
        texts[i]
        for i in range(len(texts))
        if i not in corpus_result["blocked_indices"]
    ]
    return safe_texts


def main():
    sample_texts = [
        "Python is a great programming language for beginners.",
        "The weather today is sunny and warm.",
    ]

    try:
        result = check_corpus_safety(sample_texts)
        print(f"Corpus safety check (Azure AI Content Safety):")
        print(f"  Total: {result['total']}")
        print(f"  Safe: {result['safe_count']}")
        print(f"  Blocked: {result['blocked_count']}")
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to use this module.")


if __name__ == "__main__":
    main()
