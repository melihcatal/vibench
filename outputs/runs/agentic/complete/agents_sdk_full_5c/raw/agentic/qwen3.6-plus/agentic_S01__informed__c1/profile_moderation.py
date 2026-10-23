"""
Moderate profile text before account activation.

Provider: Azure AI Content Safety
Provider-identifying signals:
  - requests SDK with Azure-specific Content Safety API endpoint
  - AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars
  - api.cognitive.microsoft.com / contentsafety hostname
  - Azure-specific risk level categories (Hate, SelfHarm, Sexual, Violence)
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error

from identity_models import serialize_response

logger = logging.getLogger(__name__)

AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"

CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def _get_endpoint() -> str:
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV, "").rstrip("/")
    if not endpoint:
        raise ValueError(
            f"Missing {AZURE_CONTENT_SAFETY_ENDPOINT_ENV}. "
            "Set your Azure Content Safety endpoint (e.g. "
            "https://<resource>.cognitiveservices.azure.com)."
        )
    return endpoint


def _get_api_key() -> str:
    api_key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"Missing {AZURE_CONTENT_SAFETY_KEY_ENV}. Set your Azure "
            "Content Safety API key."
        )
    return api_key


def _analyze_text_with_azure(text: str, output_type: str = "EightSeverityLevels") -> Dict[str, Any]:
    """
    Call Azure AI Content Safety AnalyzeText API.

    Endpoint: POST {endpoint}/contentsafety/text:analyze?api-version={version}
    """
    endpoint = _get_endpoint()
    api_key = _get_api_key()
    url = (
        f"{endpoint}/contentsafety/text:analyze"
        f"?api-version={CONTENT_SAFETY_API_VERSION}"
    )

    payload = json.dumps({
        "text": text,
        "outputType": output_type,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        logger.error(
            "Azure AI Content Safety HTTP error %s: %s",
            e.code,
            body,
        )
        raise
    except Exception as e:
        logger.error("Azure AI Content Safety request failed: %s", str(e))
        raise


def _extract_categories_and_severity(analysis: Dict[str, Any]) -> Dict[str, int]:
    """
    Extract severity levels per category from Azure Content Safety response.
    Categories: Hate, SelfHarm, Sexual, Violence.
    Returns dict like {"Hate": 0, "SelfHarm": 0, "Sexual": 2, "Violence": 0}.
    """
    categories = {}
    for cat_result in analysis.get("categoriesAnalysis", []):
        category = cat_result.get("category", "Unknown")
        severity = cat_result.get("severity", 0)
        categories[category] = severity
    return categories


def moderate_profile_text(
    profile_text: str,
    max_severity: int = 2,
) -> Dict[str, Any]:
    """
    Moderate user profile text using Azure AI Content Safety.

    Analyzes text for four content safety categories (Hate, SelfHarm,
    Sexual, Violence) and checks severity against the max allowed level.

    Azure severity scale: 0 (safe) to 6 (most severe).

    Args:
        profile_text: The user profile text to moderate.
        max_severity: Maximum allowed severity per category (default 2).

    Returns:
        Dict with moderation verdict, category severities, and flag info.
    """
    analysis = _analyze_text_with_azure(profile_text)
    categories = _extract_categories_and_severity(analysis)

    flagged = {}
    is_approved = True

    for category, severity in categories.items():
        if severity > max_severity:
            is_approved = False
            flagged[category] = severity

    verdict = "approved" if is_approved else "flagged"

    logger.info(
        "Azure AI Content Safety: moderation verdict=%s, text_length=%d, categories=%s",
        verdict,
        len(profile_text),
        categories,
    )

    return {
        "verdict": verdict,
        "approved": is_approved,
        "categories": categories,
        "flagged_categories": flagged,
        "max_severity": max_severity,
        "text_length": len(profile_text),
        "provider": "azure_ai_content_safety",
    }


def moderate_profile_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience wrapper accepting a dict and returning a dict."""
    return moderate_profile_text(
        profile_text=data["profile_text"],
        max_severity=data.get("max_severity", 2),
    )
