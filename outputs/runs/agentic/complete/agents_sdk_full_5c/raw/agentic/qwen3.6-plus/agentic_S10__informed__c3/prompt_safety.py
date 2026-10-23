"""
Check prompts and generated text for unsafe content using Azure AI Content Safety.

Provider: Azure AI Content Safety
SDK: requests (REST)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

import requests

from model_models import SafetyResult


AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def load_azure_content_safety_config() -> dict:
    """Load Azure AI Content Safety configuration from environment."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "environment variables are required. "
            "Configure them via Azure Portal > AI Content Safety resource."
        )
    return {"endpoint": endpoint.rstrip("/"), "key": key}


def _build_safety_url(endpoint: str, api_version: str = AZURE_CONTENT_SAFETY_API_VERSION) -> str:
    """Construct the Azure AI Content Safety text analysis URL."""
    return f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"


def check_safety(
    text: str,
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> SafetyResult:
    """Analyze text for unsafe content using Azure AI Content Safety.

    Args:
        text: The text to check (prompt or generated output).
        categories: Optional list of severity levels to check, e.g. ["Hate", "SelfHarm"].
            Default categories: Hate, SelfHarm, Sexual, Violence.
        endpoint: Override Azure Content Safety endpoint URL.
        key: Override Azure Content Safety key.

    Returns:
        SafetyResult indicating whether the text is safe and per-category scores.
    """
    config = load_azure_content_safety_config()
    url = endpoint or config["endpoint"]
    api_key = key or config["key"]
    analysis_url = _build_safety_url(url)

    default_categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    target_categories = categories or default_categories

    payload = {
        "text": text,
        "categories": target_categories,
        "outputType": "FourSeverityLevels",
    }

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    response = requests.post(analysis_url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result_data = response.json()

    return _parse_safety_response(result_data)


def _parse_safety_response(result_data: dict) -> SafetyResult:
    """Parse Azure AI Content Safety response into normalized SafetyResult."""
    categories: Dict[str, float] = {}
    flagged: List[str] = []
    is_safe = True

    category_scores_map = {
        "Hate": 0,
        "SelfHarm": 0,
        "Sexual": 0,
        "Violence": 0,
    }

    severity_to_score = {
        "Safe": 0,
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Unknown": 0,
    }

    analysis_result = result_data.get("analysisResult", {})
    for cat_result in analysis_result.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "Unknown")
        severity = cat_result.get("severity", "Safe")
        score = severity_to_score.get(severity, 0)
        categories[cat_name] = score
        if score >= 2:  # Medium or High
            flagged.append(cat_name)
            is_safe = False

    # Also check blocklists if present
    blocklists = result_data.get("blocklistsMatch", [])
    if blocklists:
        is_safe = False
        for bl in blocklists:
            flagged.append(f"blocklist:{bl.get('blocklistName', 'unknown')}")

    return SafetyResult(
        is_safe=is_safe,
        categories=categories,
        flagged_categories=flagged,
        raw_response=result_data,
    )


def check_prompt_safety(prompt: str) -> SafetyResult:
    """Convenience function to check a user prompt for safety."""
    return check_safety(prompt)


def check_output_safety(generated_text: str) -> SafetyResult:
    """Convenience function to check generated model output for safety."""
    return check_safety(generated_text)


def check_both(
    prompt: str,
    generated_text: str,
) -> tuple[SafetyResult, SafetyResult]:
    """Check both the prompt and generated output for unsafe content."""
    prompt_result = check_safety(prompt)
    output_result = check_safety(generated_text)
    return prompt_result, output_result
