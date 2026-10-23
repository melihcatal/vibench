import os
import requests
from observability_models import SafetyCheckResult

API_ENDPOINT = "https://api.perspectiveapi.com/v1/analyze"
API_KEY = os.getenv("PERSPECTIVE_API_KEY")

if not API_KEY:
    raise RuntimeError("PERSPECTIVE_API_KEY environment variable is not set")


def check_safety(text: str, attribute: str = "TOXICITY") -> SafetyCheckResult:
    """Check selected log message text for unsafe content using Perspective API.
    Returns a SafetyCheckResult indicating if the text is flagged and severity.
    """
    payload = {"comment": {"text": text}, "requestedAttributes": {attribute: {}}}
    headers = {"x-api-key": API_KEY}
    response = requests.post(API_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    score = (
        result.get("attributeScores", {})
        .get(attribute, {})
        .get("summaryScore", {})
        .get("value")
    )
    flagged = score and score >= 0.5  # simple threshold
    return SafetyCheckResult(
        flagged=flagged, severity=round(score or 0, 2), attribute=attribute
    )
