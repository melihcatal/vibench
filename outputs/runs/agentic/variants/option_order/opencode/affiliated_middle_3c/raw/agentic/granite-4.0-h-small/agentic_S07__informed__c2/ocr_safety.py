# ocr_safety.py
# LATER-STEP file
# Checks OCR-extracted text for unsafe content using Perspective API (REST) [example]

import json
import requests
from document_models import SafetyCheckResult

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")

PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def analyze_content(text: str) -> SafetyCheckResult:
    """Run Perspective API toxicity check on OCR output.

    Args:
        text: Plain text extracted from document.

    Returns:
        SafetyCheckResult indicating safe status and any flagged categories.
    """
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {"content-type": "application/json", "x-api-key": PERSPECTIVE_API_KEY}
    response = requests.post(
        PERSPECTIVE_ENDPOINT, data=json.dumps(payload), headers=headers
    )
    response.raise_for_status()
    data = response.json()
    attribute_score = data.get("attributeScores", {}).get("TOXICITY", {})
    severity = attribute_score.get("summaryScore", {}).get("value")
    safe = severity < 0.5  # threshold can be tuned
    flagged = [] if safe else ["TOXICITY"]
    return SafetyCheckResult(safe=safe, flagged=flagged)
