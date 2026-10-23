"""
Check extracted document text for unsafe content using Azure AI Content Safety.
Uses the Azure AI Content Safety REST API for text moderation and safety analysis.
"""

import os
from typing import Dict, List, Optional

import requests

from document_models import DocumentTextResult

# Azure AI Content Safety API hostname
AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def get_azure_content_safety_endpoint() -> str:
    """Retrieve Azure Content Safety endpoint from environment."""
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    if not endpoint:
        raise ValueError(f"{AZURE_CONTENT_SAFETY_ENDPOINT_ENV} environment variable is required")
    # Ensure endpoint has no trailing slash
    return endpoint.rstrip("/")


def get_azure_content_safety_key() -> str:
    """Retrieve Azure Content Safety API key from environment."""
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)
    if not key:
        raise ValueError(f"{AZURE_CONTENT_SAFETY_KEY_ENV} environment variable is required")
    return key


def check_text_safety(
    text: str,
    categories: Optional[List[str]] = None,
    halt_on_severity: int = 4,
) -> Dict:
    """
    Check a text string for unsafe content using Azure AI Content Safety API.

    Analyzes text for hate, self-harm, sexual, and violence categories.

    Args:
        text: The text content to analyze for safety.
        categories: Optional list of categories to check. Default checks all four.
        halt_on_severity: Severity threshold (0-7) above which content is flagged.

    Returns:
        Dict: Safety analysis result with category scores and flagged status.
    """
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    endpoint = get_azure_content_safety_endpoint()
    key = get_azure_content_safety_key()
    url = f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    result = response.json()

    # Determine if content is flagged
    flagged = False
    category_results = {}
    for cat_result in result.get("blocklistsMatch", []):
        flagged = True
        category_results[cat_result.get("category", "")] = cat_result

    for cat_result in result.get("analysisResult", []):
        category_name = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        category_results[category_name] = severity
        if severity >= halt_on_severity:
            flagged = True

    return {
        "flagged": flagged,
        "categories": category_results,
        "raw_response": result,
    }


def check_ocr_result_safety(
    ocr_result: DocumentTextResult,
    categories: Optional[List[str]] = None,
    halt_on_severity: int = 4,
) -> Dict:
    """
    Check OCR-extracted document text for unsafe content using Azure AI Content Safety.

    Args:
        ocr_result: The DocumentTextResult from OCR extraction.
        categories: Optional list of categories to check.
        halt_on_severity: Severity threshold above which content is flagged.

    Returns:
        Dict: Safety analysis result for the full document text and per-block results.
    """
    # Check full text
    full_safety = check_text_safety(
        ocr_result.full_text,
        categories=categories,
        halt_on_severity=halt_on_severity,
    )

    # Check individual blocks
    block_safety_results = []
    for block in ocr_result.blocks:
        if block.content.strip():
            block_safety = check_text_safety(
                block.content,
                categories=categories,
                halt_on_severity=halt_on_severity,
            )
            block_safety_results.append({
                "block_index": len(block_safety_results),
                "content_preview": block.content[:100],
                "flagged": block_safety["flagged"],
                "categories": block_safety["categories"],
            })

    return {
        "document_flagged": full_safety["flagged"],
        "full_text_analysis": full_safety,
        "block_analyses": block_safety_results,
    }


def check_text_safety_batch(
    texts: List[str],
    categories: Optional[List[str]] = None,
    halt_on_severity: int = 4,
) -> List[Dict]:
    """
    Check multiple text strings for unsafe content using Azure AI Content Safety API.

    Args:
        texts: List of text strings to analyze.
        categories: Optional list of categories to check.
        halt_on_severity: Severity threshold above which content is flagged.

    Returns:
        List[Dict]: Safety analysis results for each text string.
    """
    return [
        check_text_safety(text, categories=categories, halt_on_severity=halt_on_severity)
        for text in texts
    ]
