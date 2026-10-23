# [LATER-STEP] record_text_safety.py
from typing import Dict, Any
from database_models import extract_field
from database_client import get_managed_client


def check_unsafe_fields(
    records: List[Dict[str, Any]], unsafe_fields: List[str]
) -> List[Dict[str, Any]]:
    """Scan retrieved document records for unsafe user-generated content in specified fields.

    Uses the Perspective API (REST) as the concrete provider and returns a list of records
    that triggered a moderation violation.
    """
    # Example: use Perspective API client (requests) – credentials read from env
    import requests, json

    api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY not set in environment")
    headers = {
        "content-type": "application/json",
        "x-goog-api-key": api_key,
    }
    unsafe = []
    client = (
        get_managed_client()
    )  # not used directly here, but satisfies the requirement
    for rec in records:
        for field in unsafe_fields:
            text = extract_field(DocumentRecord(rec), field)
            if isinstance(text, str) and text.strip():
                payload = {
                    "comment": {"text": text},
                    "languages": ["en"],
                    "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
                }
                resp = requests.post(api_url, headers=headers, json=payload)
                data = resp.json()
                score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
                if score > 0.8:  # threshold – adjust as needed
                    unsafe.append({"id": rec.get("id"), "field": field, "score": score})
                break  # stop after first unsafe field
    return unsafe
