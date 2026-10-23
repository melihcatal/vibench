"""
Check free-text metric labels or annotations for unsafe text using Azure AI Content Safety.

Analyzes metric annotations, dashboard notes, and custom labels for toxic,
hateful, or otherwise unsafe content.
Provider: Azure AI Content Safety (AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY).
"""

import os
from dataclasses import dataclass
from typing import Optional

import requests

AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"
AZURE_CONTENT_SAFETY_ANALYZE_PATH = "/contentsafety/text:analyze"


@dataclass
class SafetyAnalysisResult:
    """Result of content safety analysis."""
    text: str
    is_safe: bool
    categories: dict[str, int]
    severity_level: str
    details: str


def _get_azure_content_safety_config() -> tuple[str, str]:
    """Retrieve Azure AI Content Safety configuration from environment."""
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    if not endpoint:
        raise EnvironmentError(
            f"{AZURE_CONTENT_SAFETY_ENDPOINT_ENV} environment variable is required"
        )
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)
    if not key:
        raise EnvironmentError(
            f"{AZURE_CONTENT_SAFETY_KEY_ENV} environment variable is required"
        )
    endpoint = endpoint.rstrip("/")
    return endpoint, key


def check_annotation_safety(
    annotation_text: str,
    categories: Optional[list[str]] = None,
    output_type: str = "FourSeverityLevels",
) -> SafetyAnalysisResult:
    """
    Check a metric annotation for unsafe content using Azure AI Content Safety.

    Args:
        annotation_text: The text annotation to analyze.
        categories: Content categories to check (default: all).
        output_type: Output format for severity levels.

    Returns:
        SafetyAnalysisResult with safety assessment.
    """
    endpoint, key = _get_azure_content_safety_config()

    if categories is None:
        categories = [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence",
        ]

    url = f"{endpoint}{AZURE_CONTENT_SAFETY_ANALYZE_PATH}"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    payload = {
        "text": annotation_text,
        "output_type": output_type,
        "categories": categories,
    }

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    category_results = {}
    max_severity = 0
    for result in data.get("categoriesAnalysis", []):
        category = result.get("category", "")
        severity = result.get("severity", 0)
        category_results[category] = severity
        if severity > max_severity:
            max_severity = severity

    severity_map = {
        0: "Safe",
        2: "Low",
        4: "Medium",
        6: "High",
    }
    severity_label = severity_map.get(max_severity, "Unknown")

    is_safe = max_severity == 0

    return SafetyAnalysisResult(
        text=annotation_text,
        is_safe=is_safe,
        categories=category_results,
        severity_level=severity_label,
        details=f"Maximum severity: {severity_label} ({max_severity})",
    )


def check_multiple_annotations(
    annotations: list[str],
    categories: Optional[list[str]] = None,
) -> list[SafetyAnalysisResult]:
    """
    Check multiple metric annotations for unsafe content.

    Args:
        annotations: List of annotation texts to analyze.
        categories: Content categories to check.

    Returns:
        List of SafetyAnalysisResult objects.
    """
    results = []
    for annotation in annotations:
        result = check_annotation_safety(annotation, categories=categories)
        results.append(result)
    return results


def filter_unsafe_annotations(
    annotations: list[str],
    categories: Optional[list[str]] = None,
) -> tuple[list[str], list[SafetyAnalysisResult]]:
    """
    Filter annotations, returning only safe ones along with all safety results.

    Args:
        annotations: List of annotation texts.
        categories: Content categories to check.

    Returns:
        Tuple of (safe_annotations, all_safety_results).
    """
    results = check_multiple_annotations(annotations, categories=categories)
    safe = [
        annotation for annotation, result in zip(annotations, results)
        if result.is_safe
    ]
    return safe, results
