import json
import requests
from .database_client import DatabaseClient
from .database_models import DatabaseModels

# Perspective API JSON endpoint (example) – replace with your real key
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
# You must set env var PERSPECTIVE_API_KEY before running
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_toxicity(text: str) -> Dict[str, Any]:
    """Send text to Perspective API and return the JSON toxicity scores.
    Provider identifiable: Perspective API (requests‑based REST call, PERSPECTIVE_API_KEY env var).
    """
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {"x-api-key": PERSPECTIVE_API_KEY, "Content-Type": "application/json"}
    resp = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


def record_text_safety(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Add a 'safe' flag indicating whether the document's content passes Perspective toxicity check.
    Returns a normalized document with the safety indication.
    """
    scores = check_toxicity(doc.get("content", ""))
    toxicity = (
        scores.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0.0)
    )
    safe = toxicity < 0.5  # threshold can be adjusted
    doc["safe"] = safe
    return DatabaseModels.DocumentResponse(**doc).content
