# metric_annotation_safety.py
# LATER-STEP: Check free-text metric labels or annotations for unsafe text

import os
import requests
from typing import Any, Dict

# Example: Uses Perspective API to scan strings for toxicity
# Perspective API endpoint & key are configured via env vars
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")


def _perspective_scan(text: str) -> Dict[str, Any]:
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "PROFANITY": {}}
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": PERSPECTIVE_API_KEY
    }
    resp = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


def is_metric_annotation_safe(annotation: str, threshold: float = 0.5) -> bool:
    """
    Returns True if the annotation is deemed safe (toxicity < threshold).
    Perspects API returns scores between 0.0 (safe) and 1.0 (unsafe).
    """
    resp = _perspective_scan(annotation)
    attributes = resp.get('attributeScores', {})
    toxicity_score = attributes.get('TOXICITY', {'summaryScore': {'value': 0.0}})['summaryScore']['value']
    severe_toxicity = attributes.get('SEVERE_TOXICITY', {'summaryScore': {'value': 0.0}})['summaryScore']['value']
    profanity = attributes.get('PROFANITY', {'summaryScore': {'value': 0.0}})['summaryScore']['value']
    # If any severe signal exceeds threshold, flag as unsafe
    if severe_toxicity >= threshold or profanity >= threshold:
        return False
    return True

# ---------------------------------------------------------------------------
# Example usage (can be called from other services)
if __name__ == "__main__":
    test_annotation = "This metric is broken, fix it now!"
    safe = is_metric_annotation_safe(test_annotation)
    print(f"Annotation safe? {safe}")
