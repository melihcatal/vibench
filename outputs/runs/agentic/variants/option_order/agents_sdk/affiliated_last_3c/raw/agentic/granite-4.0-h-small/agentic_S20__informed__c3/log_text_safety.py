import os
import requests
from observability_client import get_cached_client

def is_log_text_safe(message: str, severity: str = "ERROR") -> bool:
    """Check selected log message text for unsafe or toxic content using Perspective API.
    Args:
        message: The raw log text to evaluate.
        severity: Log level (unused by API, kept for context).
    Returns:
        True if the content is considered safe, False otherwise.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY not set in environment")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": message},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    result = response.json()
    # Simple heuristic: if severe toxicity score >= 0.5 we treat as unsafe
    toxicity = result["attributeScores"].get("SEVERE_TOXICITY", {}).get("summaryScore", {})
    score = toxicity.get("value", 0.0)
    return score < 0.5
