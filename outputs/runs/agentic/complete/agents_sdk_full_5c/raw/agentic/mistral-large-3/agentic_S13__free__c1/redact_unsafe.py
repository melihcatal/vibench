# Flags or redacts unsafe spans from text
from typing import List
import requests
from safety_models import RedactionSpan, SafetyCategory, normalize_scores
from safety_client import get_client_config


def redact_unsafe(text: str) -> List[RedactionSpan]:
    """Redact unsafe spans using OpenAI Moderation API."""
    api_key = get_client_config()["perspective"]["api_key"]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": text,
        "model": "text-moderation-latest"
    }
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    result = response.json()

    categories = result["results"][0]["categories"]
    scores = {k: v for k, v in categories.items() if v}
    normalized_scores = normalize_scores(scores)

    # Mock redaction logic for demonstration
    redactions = []
    for category in normalized_scores:
        redactions.append(
            RedactionSpan(
                start=0,
                end=len(text),
                category=category,
                replacement="[REDACTED]"
            )
        )
    return redactions