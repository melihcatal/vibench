"""
Check secret labels and notes for unsafe text using Azure AI Content Safety API.

Analyzes secret labels, descriptions, and attached notes for potentially unsafe
content including hate speech, self-harm, sexual content, and violence.

Provider: Azure AI Content Safety
SDK: azure-ai-contentsafety / requests (REST)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
import json
from typing import Optional, Dict, Any, List

import requests

# Azure AI Content Safety provider configuration
AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def _get_azure_content_safety_endpoint() -> str:
    """Retrieve Azure Content Safety endpoint from environment."""
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    if not endpoint:
        raise ValueError(
            f"Set the {AZURE_CONTENT_SAFETY_ENDPOINT_ENV} environment variable "
            f"with your Azure AI Content Safety resource endpoint."
        )
    # Ensure endpoint doesn't have a trailing slash
    return endpoint.rstrip("/")


def _get_azure_content_safety_key() -> str:
    """Retrieve Azure Content Safety API key from environment."""
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)
    if not key:
        raise ValueError(
            f"Set the {AZURE_CONTENT_SAFETY_KEY_ENV} environment variable "
            f"with your Azure AI Content Safety API key."
        )
    return key


def analyze_text_safety(
    text: str,
    blocklists: Optional[List[str]] = None,
    halt_on_blocklist_hit: bool = False,
) -> Dict[str, Any]:
    """
    Analyze text content using Azure AI Content Safety Text Analysis API.

    Args:
        text: The text content to analyze for safety.
        blocklists: Optional list of custom blocklist names to check against.
        halt_on_blocklist_hit: Whether to stop analysis on blocklist match.

    Returns:
        Dictionary with safety analysis results including category scores.
    """
    endpoint = _get_azure_content_safety_endpoint()
    api_key = _get_azure_content_safety_key()

    url = f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload: Dict[str, Any] = {"text": text}

    if blocklists:
        payload["blocklists"] = blocklists
        payload["haltOnBlocklistHit"] = halt_on_blocklist_hit

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result_data = response.json()

        categories = result_data.get("categoriesAnalysis", [])
        category_results = {}
        max_severity = 0

        for cat in categories:
            cat_name = cat.get("category", "unknown")
            severity = cat.get("severity", 0)
            category_results[cat_name] = {
                "severity": severity,
                "is_flagged": severity >= 4,  # Azure: 0=Safe, 2=Low, 4=Medium, 6=High
            }
            max_severity = max(max_severity, severity)

        blocklist_result = result_data.get("blocklistsMatch", [])

        overall_unsafe = max_severity >= 4 or bool(blocklist_result)

        return {
            "success": True,
            "text_analyzed": True,
            "is_unsafe": overall_unsafe,
            "max_severity": max_severity,
            "categories": category_results,
            "blocklist_matches": blocklist_result,
            "provider": "azure_ai_content_safety",
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error_code": "AZURE_CONTENT_SAFETY_API_ERROR",
            "error_message": str(e),
            "provider": "azure_ai_content_safety",
        }


def check_secret_labels_safety(
    labels: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Check multiple secret labels and notes for unsafe content.

    Args:
        labels: List of dicts with 'secret_id' and 'label_text' keys.

    Returns:
        Dictionary with per-label safety analysis and overall summary.
    """
    results = []
    total_unsafe = 0

    for label in labels:
        secret_id = label.get("secret_id", "unknown")
        label_text = label.get("label_text", "")

        if not label_text.strip():
            results.append({
                "secret_id": secret_id,
                "is_unsafe": False,
                "categories": {},
                "max_severity": 0,
                "skipped": True,
                "reason": "Empty label text",
            })
            continue

        safety_result = analyze_text_safety(label_text)

        label_result = {
            "secret_id": secret_id,
            "is_unsafe": safety_result.get("is_unsafe", False),
            "categories": safety_result.get("categories", {}),
            "max_severity": safety_result.get("max_severity", 0),
            "provider": "azure_ai_content_safety",
        }

        if not safety_result.get("success"):
            label_result["error"] = safety_result.get("error_message", "Unknown error")

        if safety_result.get("is_unsafe"):
            total_unsafe += 1

        results.append(label_result)

    return {
        "success": True,
        "total_labels_checked": len(labels),
        "unsafe_labels_found": total_unsafe,
        "safe_labels_found": len(labels) - total_unsafe,
        "labels": results,
        "provider": "azure_ai_content_safety",
    }
