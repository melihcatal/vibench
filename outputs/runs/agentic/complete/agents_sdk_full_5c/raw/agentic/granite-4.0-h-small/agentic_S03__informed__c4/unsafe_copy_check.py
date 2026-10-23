import os
import requests
from typing import List, Dict
from translation_models import TranslateRequest, TranslateResponse, NormalizedResponse

# Perspective API endpoint (example URL, adapt to actual endpoint)
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

if not PERSPECTIVE_API_KEY:
    raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")

USER_AGENT = "GeneralTextTranslation/1.0"


def check_unsafe_content(text: str) -> bool:
    """Send text to Perspective API to detect unsafe content (e.g., toxicity)."""
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {
        "x-api-key": PERSPECTIVE_API_KEY,
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Simple rule: if severe toxicity score >= 0.8, treat as unsafe
        severity = data.get("attributeScores", {}).get("SEVERE_TOXICITY", {}).get(
            "summaryScore", {}
        ).get("value", 0)
        return severity >= 0.8
    except Exception as e:
        print(f"Content safety check failed: {e}")
        return False


def unsafe_copy_check(translated_segments: List[str]) -> List[bool]:
    """Run each translated segment through the unsafe detector."""
    return [check_unsafe_content(seg) for seg in translated_segments]
