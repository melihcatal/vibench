import os
import requests
from speech_models import ModerationRequest, ModerationResponse
from typing import Any, Dict

# Perspective API example (REST)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def moderate_transcript(text: str) -> ModerationResponse:
    """Run content moderation on transcript text using Perspective API.

    Args:
        text (str): Transcript segment to evaluate.

    Returns:
        ModerationResponse: Verdict and reasons.
    """
    if not PERSPECTIVE_API_KEY:
        raise RuntimeError(
            "Perspective API key not set. Define PERSPECTIVE_API_KEY environment variable."
        )
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {
        "X-Goog-Api-Key": PERSPECTIVE_API_KEY,
        "Content-Type": "application/json; charset=utf-8",
    }
    try:
        response = requests.post(PERSPECTIVE_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        attribute_scores = data["attributeScores"]
        toxicity_score = attribute_scores.get("TOXICITY", {}).get("summaryScore", {})
        is_blocked = toxicity_score.get("value", 0) >= 0.5  # threshold example
        reasons = []
        if is_blocked:
            reasons = ["High toxicity detected"]
        return ModerationResponse(is_blocked=is_blocked, reasons=reasons, raw=data)
    except requests.RequestException as exc:
        raise RuntimeError(f"Moderation request failed: {exc}")


# Wrapper for model object


def moderate_using_model(request: ModerationRequest) -> ModerationResponse:
    return moderate_transcript(request.text)
