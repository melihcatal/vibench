import os
from database_client import get_client
from database_models import DocumentModel

def record_text_safety(document_id, text_field):
    """Check a text field for unsafe content using Perspective API (external provider).
    Returns True if safe, False if unsafe.
    """
    # Example implementation using REST request to Perspective API
    import requests, json
    client = get_client()  # not used directly here; just for shared config pattern
    text = fetch_document(document_id)[text_field]
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("PERSPECTIVE_API_KEY must be set")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "THREAT": {}, "INSULT": {}, "PROFANITY": {}}
    }
    headers = {"key": api_key, "content-type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    scores = resp.json()["attributeScores"]
    # Simple rule: if any attribute exceeds 0.9, consider unsafe
    unsafe = any(s["summaryScore"]["value"] > 0.9 for s in scores.values())
    return not unsafe
