import os
from typing import Optional

import requests

from safety_models import (
    AZURE_CONTENT_SAFETY_CATEGORIES,
    BatchModerationRequest,
    BatchModerationResponse,
    SafetyResponse,
    build_azure_payload,
    parse_azure_response,
)

AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def get_azure_endpoint() -> str:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    if not endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required. "
            "Set it to your Azure AI Content Safety resource endpoint, e.g. "
            "https://<your-resource>.cognitiveservices.azure.com/"
        )
    return endpoint


def get_azure_key() -> str:
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    if not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY environment variable is required. "
            "Set it to your Azure AI Content Safety resource key."
        )
    return key


def _build_analyze_url() -> str:
    endpoint = get_azure_endpoint()
    return (
        f"{endpoint}/contentsafety/text:analyze"
        f"?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    )


def _make_request(payload: dict) -> dict:
    url = _build_analyze_url()
    headers = {
        "Ocp-Apim-Subscription-Key": get_azure_key(),
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def analyze_text(text: str, categories: list[str] | None = None) -> SafetyResponse:
    if categories is None:
        categories = AZURE_CONTENT_SAFETY_CATEGORIES
    payload = build_azure_payload(text, categories)
    raw = _make_request(payload)
    return parse_azure_response(text, raw)


def analyze_batch(
    request: BatchModerationRequest,
    categories: list[str] | None = None,
) -> BatchModerationResponse:
    if categories is None:
        categories = AZURE_CONTENT_SAFETY_CATEGORIES
    results: list[SafetyResponse] = []
    for text in request.texts:
        result = analyze_text(text, categories)
        results.append(result)
    return BatchModerationResponse(results=results)


def analyze_text_with_blocklist(
    text: str,
    blocklist_name: Optional[str] = None,
    categories: list[str] | None = None,
) -> SafetyResponse:
    endpoint = get_azure_endpoint()
    url = (
        f"{endpoint}/contentsafety/text:analyze"
        f"?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    )
    payload = build_azure_payload(text, categories)
    if blocklist_name:
        payload["blocklistNames"] = [blocklist_name]
    headers = {
        "Ocp-Apim-Subscription-Key": get_azure_key(),
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    raw = response.json()
    return parse_azure_response(text, raw)
