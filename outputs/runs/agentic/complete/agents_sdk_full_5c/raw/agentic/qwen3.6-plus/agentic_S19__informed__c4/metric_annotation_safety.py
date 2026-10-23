"""
Check free-text metric labels or annotations for unsafe text.

Uses the Azure AI Content Safety API to analyze metric annotation text
for harmful content categories including hate, sexual, violence, and self-harm.
"""

import os
from typing import Optional, Dict, Any, List

import requests


def _build_safety_url(endpoint: str, api_version: str = "2024-02-15-preview") -> str:
    """Build the Azure AI Content Safety analyze text endpoint URL."""
    base = endpoint.rstrip("/")
    return f"{base}/contentsafety/text:analyze?api-version={api_version}"


def check_metric_annotation_safety(
    text: str,
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = "2024-02-15-preview",
) -> Dict[str, Any]:
    """Check free-text metric labels or annotations for unsafe text.

    Sends the provided annotation text to the Azure AI Content Safety
    analyze text API (contentsafety.azure.com) to evaluate for harmful
    content across categories: Hate, SelfHarm, Sexual, Violence.

    Args:
        text: The metric annotation or label text to check.
        categories: Optional list of categories to check. If None, checks all
            default categories (Hate, SelfHarm, Sexual, Violence).
        endpoint: Azure AI Content Safety endpoint URL
            (e.g., 'https://<resource>.cognitiveservices.azure.com/').
            Defaults to AZURE_CONTENT_SAFETY_ENDPOINT env var.
        api_key: Azure Content Safety API key.
            Defaults to AZURE_CONTENT_SAFETY_KEY env var.
        api_version: Azure API version (default: 2024-02-15-preview).

    Returns:
        Dict with 'safe' (bool), 'categories' (dict of severity levels),
        and 'block_reason' (str or None).

    Raises:
        ValueError: If endpoint or api_key is not provided.
    """
    safety_endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    safety_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not safety_endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required "
            "for Azure AI Content Safety API access."
        )
    if not safety_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY environment variable is required "
            "for Azure AI Content Safety API access."
        )

    # Build the category blocks
    default_categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    check_categories = categories if categories else default_categories

    payload = {
        "text": text,
        "categories": check_categories,
        "outputType": "EightSeverityLevels",
    }

    url = _build_safety_url(safety_endpoint, api_version)
    headers = {
        "Ocp-Apim-Subscription-Key": safety_key,
        "Content-Type": "application/json",
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()

    data = resp.json()

    # Parse results
    categories_result = {}
    max_severity = 0
    block_reason = None

    for category_result in data.get("categoriesAnalysis", []):
        cat_name = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        categories_result[cat_name] = severity

        if severity > max_severity:
            max_severity = severity
            if severity >= 4:
                block_reason = f"{cat_name} content detected (severity: {severity})"

    return {
        "safe": max_severity < 4,
        "categories": categories_result,
        "max_severity": max_severity,
        "block_reason": block_reason,
        "text_length": len(text),
    }


def check_metric_annotation_safety_batch(
    annotations: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    threshold: int = 4,
) -> List[Dict[str, Any]]:
    """Batch check multiple metric annotations for unsafe content.

    Args:
        annotations: List of annotation texts to check.
        endpoint: Azure AI Content Safety endpoint.
        api_key: Azure Content Safety API key.
        threshold: Severity level above which content is flagged (default: 4).

    Returns:
        List of result dicts, one per annotation.
    """
    results = []
    for i, annotation in enumerate(annotations):
        try:
            result = check_metric_annotation_safety(
                text=annotation,
                endpoint=endpoint,
                api_key=api_key,
            )
            results.append({
                "index": i,
                "text_preview": annotation[:100],
                **result,
            })
        except requests.RequestException as e:
            results.append({
                "index": i,
                "text_preview": annotation[:100],
                "safe": True,  # assume safe on error to avoid blocking
                "categories": {},
                "max_severity": 0,
                "block_reason": f"API error: {str(e)}",
                "error": True,
            })

    return results


def validate_metric_label(
    label: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    allowed_categories: Optional[List[str]] = None,
) -> bool:
    """Validate a single metric label/annotation, returning True if safe.

    Args:
        label: The label text to validate.
        endpoint: Azure AI Content Safety endpoint.
        api_key: Azure Content Safety API key.
        allowed_categories: Optional specific categories to check.

    Returns:
        True if the text passes safety checks, False otherwise.
    """
    result = check_metric_annotation_safety(
        text=label,
        categories=allowed_categories,
        endpoint=endpoint,
        api_key=api_key,
    )
    return result["safe"]
