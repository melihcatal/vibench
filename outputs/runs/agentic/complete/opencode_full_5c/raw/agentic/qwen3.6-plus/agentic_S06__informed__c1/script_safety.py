import os
import httpx
from typing import List, Optional
from speech_models import (
    SafetyCheckRequest,
    SafetyCheckResponse,
    normalize_safety_response,
)


PERSPECTIVE_API_BASE = "https://commentanalyzer.googleapis.com/v1alpha1"


def check_script_safety(
    text: str,
    languages: List[str] = None,
    attributes: List[str] = None,
    threshold: float = 0.5,
    api_key: Optional[str] = None,
) -> SafetyCheckResponse:
    key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
    if not key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set")
    langs = languages or ["en"]
    attrs = attributes or [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "IDENTITY_ATTACK",
        "INSULT",
        "PROFANITY",
        "THREAT",
    ]
    requested_attrs = {attr: {} for attr in attrs}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attrs,
        "languages": langs,
        "doNotStore": True,
    }
    url = f"{PERSPECTIVE_API_BASE}/comments:analyze"
    params = {"key": key}
    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, json=payload, params=params)
        response.raise_for_status()
        data = response.json()
    return normalize_safety_response(data, text)


def check_script_safety_batch(
    texts: List[str],
    languages: List[str] = None,
    attributes: List[str] = None,
    api_key: Optional[str] = None,
) -> List[SafetyCheckResponse]:
    responses = []
    for text in texts:
        responses.append(
            check_script_safety(
                text,
                languages=languages,
                attributes=attributes,
                api_key=api_key,
            )
        )
    return responses
