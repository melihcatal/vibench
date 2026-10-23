"""
Local configuration and client helper utilities for Text Content Safety
using Azure AI Content Safety.
"""

import os
from typing import Any, Dict, List, Optional

# Provider-specific environment variables for Azure AI Content Safety
AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def get_azure_content_safety_config() -> Dict[str, str]:
    """Load Azure AI Content Safety configuration from environment variables."""
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)
    if not endpoint or not key:
        raise ValueError(
            f"Both {AZURE_CONTENT_SAFETY_ENDPOINT_ENV} and "
            f"{AZURE_CONTENT_SAFETY_KEY_ENV} must be set."
        )
    return {
        "endpoint": endpoint.rstrip("/"),
        "key": key,
        "api_version": AZURE_CONTENT_SAFETY_API_VERSION,
    }


def build_azure_auth_headers(api_key: str) -> Dict[str, str]:
    """Build the authorization headers required by Azure AI Content Safety REST API."""
    return {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }


def build_moderation_payload(text: str) -> Dict[str, Any]:
    """Build the JSON payload for the Azure AI Content Safety Text:Analyze endpoint."""
    return {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "EightSeverityLevels",
    }


def build_batch_moderation_payload(texts: List[str]) -> Dict[str, Any]:
    """Build the JSON payload for the Azure AI Content Safety Text:AnalyzeBatch endpoint."""
    return {
        "text": texts,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "EightSeverityLevels",
    }


def create_azure_content_safety_session(config: Optional[Dict[str, str]] = None):
    """Create and return a requests Session pre-configured for Azure AI Content Safety."""
    import requests

    cfg = config or get_azure_content_safety_config()
    session = requests.Session()
    session.headers.update(build_azure_auth_headers(cfg["key"]))
    return session, cfg


def get_analyze_text_url(cfg: Dict[str, str]) -> str:
    """Return the Azure AI Content Safety analyze-text REST endpoint URL."""
    return (
        f"{cfg['endpoint']}/contentsafety/text:analyze"
        f"?api-version={cfg['api_version']}"
    )


def get_analyze_batch_url(cfg: Dict[str, str]) -> str:
    """Return the Azure AI Content Safety analyze-text batch endpoint URL."""
    return (
        f"{cfg['endpoint']}/contentsafety/text:analyzeBatch"
        f"?api-version={cfg['api_version']}"
    )
