"""
Check generated visual labels for unsafe text using Azure AI Content Safety.

Provider: Azure AI Content Safety
SDK: azure-ai-contentsafety / REST
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
import re
from typing import List, Optional, Dict, Any

import requests

from detect_image_labels import LabelDetectionResponse
from detect_image_text import TextDetectionResponse, format_text_summary


_AZURE_CONTENT_SAFETY_API_VERSION = "2024-09-01"


def check_visual_labels_text(
    labels_response: Optional[LabelDetectionResponse] = None,
    text_response: Optional[TextDetectionResponse] = None,
    content_safety_endpoint: Optional[str] = None,
    content_safety_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check generated visual labels and detected image text for unsafe content.

    Uses Azure AI Content Safety to analyze the text extracted from image
    labels and OCR results for hate speech, sexual content, violence, and
    self-harm categories.

    Args:
        labels_response: Output from detect_image_labels.
        text_response: Output from detect_image_text.
        content_safety_endpoint: Azure Content Safety endpoint override.
        content_safety_key: Azure Content Safety key override.

    Returns:
        Dict with safety analysis results per category.
    """
    endpoint = content_safety_endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = content_safety_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable must be set")
    if not key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable must be set")

    # Collect all text from labels and detected text
    text_to_analyze = _collect_text_from_analysis(labels_response, text_response)

    if not text_to_analyze:
        return {
            "analyzed": False,
            "reason": "No text content to analyze",
            "categories": {},
            "overall_safe": True,
        }

    # Join all text content for analysis
    combined_text = " ".join(text_to_analyze)

    # Call Azure AI Content Safety REST API
    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze"
    params = {"api-version": _AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    body = {
        "text": combined_text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence",
        ],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, params=params, headers=headers, json=body)
    response.raise_for_status()

    result = response.json()

    categories = {}
    overall_safe = True
    for cat_result in result.get("categoriesAnalysis", []):
        category = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        is_safe = severity <= 2
        if not is_safe:
            overall_safe = False
        categories[category] = {
            "severity": severity,
            "safe": is_safe,
            "label": _severity_label(severity),
        }

    return {
        "analyzed": True,
        "text_analyzed": combined_text[:500],
        "categories": categories,
        "overall_safe": overall_safe,
    }


def _collect_text_from_analysis(
    labels_response: Optional[LabelDetectionResponse] = None,
    text_response: Optional[TextDetectionResponse] = None,
) -> List[str]:
    """Collect all text content from label detection and text detection responses."""
    texts = []

    if labels_response:
        for label in labels_response.labels:
            texts.append(label.name)
            for parent in label.parents:
                texts.append(parent)

    if text_response:
        for detected in text_response.detected_texts:
            if detected.text.strip():
                texts.append(detected.text)

    return texts


def _severity_label(severity: int) -> str:
    """Convert Azure Content Safety numeric severity to a human-readable label."""
    labels = {
        0: "Safe",
        2: "Low",
        4: "Medium",
        6: "High",
    }
    return labels.get(severity, f"Severity-{severity}")


def format_text_safety_report(safety_result: Dict[str, Any]) -> str:
    """Format the text safety analysis results into a human-readable report."""
    if not safety_result.get("analyzed"):
        return f"Text safety check skipped: {safety_result.get('reason', 'unknown')}"

    lines = ["Visual text safety analysis results:"]

    if safety_result.get("overall_safe"):
        lines.append("  Overall status: SAFE")
    else:
        lines.append("  Overall status: FLAGGED — unsafe content detected")

    lines.append("  Category breakdown:")
    for cat_name, cat_data in safety_result.get("categories", {}).items():
        safe_flag = "✓" if cat_data.get("safe") else "✗"
        lines.append(
            f"    {safe_flag} {cat_name}: {cat_data.get('label', 'N/A')} "
            f"(severity: {cat_data.get('severity', '?')})"
        )

    return "\n".join(lines)
