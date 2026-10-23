"""
Check corpus text before embedding using Azure AI Content Safety API.

Validates text inputs for safety concerns including hate speech,
violence, sexual content, and self-harm before they are sent to
an embedding model. Uses the Azure AI Content Safety REST endpoint.

Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
environment variables or explicit parameters.
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional

import requests

AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"
AZURE_CATEGORIES = ["Hate", "SelfHarm", "Sexual", "Violence"]


@dataclass
class SafetyResult:
    """
    Result of a content safety check for a single text.

    Attributes:
        text: The input text that was checked.
        is_safe: Whether the text passed all safety thresholds.
        categories: Dict mapping category name to severity level (0-7).
        flagged_categories: List of category names that exceeded threshold.
    """

    text: str
    is_safe: bool = True
    categories: dict = field(default_factory=dict)
    flagged_categories: List[str] = field(default_factory=list)


@dataclass
class CorpusSafetyReport:
    """
    Aggregate safety report for an entire text corpus.

    Attributes:
        total_checked: Number of texts analyzed.
        safe_count: Number of texts that passed safety checks.
        flagged_count: Number of texts that failed safety checks.
        results: Per-text SafetyResult objects.
    """

    total_checked: int = 0
    safe_count: int = 0
    flagged_count: int = 0
    results: List[SafetyResult] = field(default_factory=list)


def _get_azure_headers(api_key: str) -> dict:
    """Build headers for Azure AI Content Safety API requests."""
    return {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }


def _build_analysis_url(endpoint: str) -> str:
    """Build the full Azure Content Safety text analysis URL."""
    endpoint = endpoint.rstrip("/")
    return f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"


def check_text_safety(
    text: str,
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    severity_threshold: int = 4,
) -> SafetyResult:
    """
    Check a single text for safety issues via Azure AI Content Safety.

    Args:
        text: The text to analyze.
        api_key: Azure Content Safety key. Falls back to AZURE_CONTENT_SAFETY_KEY env var.
        endpoint: Azure Content Safety endpoint URL. Falls back to AZURE_CONTENT_SAFETY_ENDPOINT env var.
        severity_threshold: Minimum severity level (0-7) to flag a category.

    Returns:
        SafetyResult with category severities and safety determination.
    """
    key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    base_endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")

    if not key:
        raise ValueError("Azure Content Safety key not provided and AZURE_CONTENT_SAFETY_KEY not set")
    if not base_endpoint:
        raise ValueError(
            "Azure Content Safety endpoint not provided and AZURE_CONTENT_SAFETY_ENDPOINT not set"
        )

    url = _build_analysis_url(base_endpoint)
    headers = _get_azure_headers(key)

    payload = {
        "text": text,
        "categories": AZURE_CATEGORIES,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    categories = {}
    flagged = []
    for cat_result in data.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        categories[cat_name] = severity
        if severity >= severity_threshold:
            flagged.append(cat_name)

    return SafetyResult(
        text=text,
        is_safe=len(flagged) == 0,
        categories=categories,
        flagged_categories=flagged,
    )


def check_corpus_safety(
    texts: List[str],
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    severity_threshold: int = 4,
) -> CorpusSafetyReport:
    """
    Check an entire corpus of texts for safety issues.

    Args:
        texts: List of text strings to analyze.
        api_key: Azure Content Safety key.
        endpoint: Azure Content Safety endpoint URL.
        severity_threshold: Minimum severity to flag.

    Returns:
        CorpusSafetyReport with aggregate and per-text results.
    """
    results = []
    safe_count = 0
    flagged_count = 0

    for text in texts:
        result = check_text_safety(
            text=text,
            api_key=api_key,
            endpoint=endpoint,
            severity_threshold=severity_threshold,
        )
        results.append(result)
        if result.is_safe:
            safe_count += 1
        else:
            flagged_count += 1

    return CorpusSafetyReport(
        total_checked=len(texts),
        safe_count=safe_count,
        flagged_count=flagged_count,
        results=results,
    )


def filter_safe_texts(
    texts: List[str],
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    severity_threshold: int = 4,
) -> List[str]:
    """
    Return only the texts that pass safety checks.

    Args:
        texts: Input text corpus.
        api_key: Azure Content Safety key.
        endpoint: Azure Content Safety endpoint URL.
        severity_threshold: Minimum severity to flag.

    Returns:
        List of texts that passed all safety checks.
    """
    report = check_corpus_safety(
        texts=texts,
        api_key=api_key,
        endpoint=endpoint,
        severity_threshold=severity_threshold,
    )
    return [r.text for r in report.results if r.is_safe]
