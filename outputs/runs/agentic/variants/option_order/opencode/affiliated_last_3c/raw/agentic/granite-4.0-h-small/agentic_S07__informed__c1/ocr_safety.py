import os
import requests
from .document_client import DocumentClient
from .document_models import OCRRequest, ProviderResponse

# Perspective API integration for toxicity/unsafe content detection
# Provider identifiable by 'requests' usage and PERSPECTIVE_API_KEY env var

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_ocr(image_bytes: bytes, context: str = "") -> dict:
    """Check extracted OCR text for unsafe content using Perspective API.

    Args:
        image_bytes: Binary content of scanned document.
        context: Optional surrounding context for better scoring.

    Returns:
        Dict with scores; example: {"score": 0.73, "type": "TOXICITY"}.
    """
    client = DocumentClient()
    text = client.extract_text(image_bytes)
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "PROFANITY": {}},
    }
    headers = {"key": PERSPECTIVE_API_KEY, "Content-Type": "application/json"}
    response = requests.post(PERSPECTIVE_URL, json=payload, headers=headers)
    result = response.json()
    # Simplify to most severe score
    score = max(
        (
            result.get("attributeScores", {})
            .get(attr, {})
            .get("summaryScore", {})
            .get("value")
            for attr in ["TOXICITY", "INSULT", "PROFANITY"]
        ),
        default=0.0,
    )
    return {"score": score, "scores": result.get("attributeScores", {})}
