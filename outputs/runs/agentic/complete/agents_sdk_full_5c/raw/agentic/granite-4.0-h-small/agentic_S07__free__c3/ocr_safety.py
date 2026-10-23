import os
import requests
from document_models import OCRResponse

def scan_for_unsafe(text: str) -> bool:
    """Check extracted document text for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing PERSPECTIVE_API_KEY environment variable")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    headers = {"X-Goog-Api-Key": api_key, "Content-Type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()
    toxicity = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return toxicity > 0.5  # threshold for unsafe

# Example usage (not executed here)
# unsafe = scan_for_unsafe(extracted_text)
