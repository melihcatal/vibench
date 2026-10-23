import os
import requests
from typing import Dict

# Provider identification – text safety check (Perspective API) in this example
safety_provider = "perspective"

# Environment variable that holds the API key
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe_content(doc_id: str, content: str) -> Dict[str, Any]:
    """
    Send the supplied text to the Perspective API and return a dict containing
    the toxicity score and a boolean indicating whether the content is unsafe
    (threshold set at 0.8 for demonstration).
    """
    payload = {
        "comment": {"type": "PLAIN_TEXT", "text": content},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {"key": PERSPECTIVE_API_KEY, "content-type": "application/json"}
    resp = requests.post(BASE_URL, json=payload, headers=headers, timeout=5)
    resp.raise_for_status()
    result = resp.json()
    attribute = (
        result.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {})
    )
    score = float(attribute.get("value", 0.0))
    unsafe = score >= 0.8
    return {
        "doc_id": doc_id,
        "content": content,
        "toxicity_score": score,
        "is_unsafe": unsafe,
    }
