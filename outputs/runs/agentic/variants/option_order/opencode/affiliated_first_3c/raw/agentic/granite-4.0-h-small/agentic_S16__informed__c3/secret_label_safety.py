# secret_label_safety.py
# [LATER-STEP]
# Check secret labels/notes for unsafe text using Perspective API

import os
import requests
from typing import Dict, Any


def contains_unsafe_label(secret_meta: Dict[str, Any]) -> bool:
    """Inspect secret metadata (labels/annotations) for unsafe language using Perspective API.

    Args:
        secret_meta: A dictionary with keys 'labels' and/or 'annotations' (both dicts of string->string).

    Returns:
        True if any unsafe language is detected, False otherwise.
    """
    # Perspective API endpoint (requires API key)
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")

    # Collect all text from labels and annotations
    texts = []
    for namespace, kv in (secret_meta.get("labels", {}),):
        texts.append(str(kv))
    for namespace, kv in (secret_meta.get("annotations", {}),):
        texts.append(str(kv))

    if not texts:
        return False  # nothing to check

    payload = {
        "comment": {"text": "\\n".join(texts)},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_HATE": {},
        },
    }

    headers = {"key": api_key, "Content-Type": "application/json"}

    try:
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        analysis = resp.json()["attributeScores"]
        # If any attribute score is above threshold, treat as unsafe
        for attr, scores in analysis.items():
            score = scores.get("summaryScore", {}).get("value", 0.0)
            if score >= 0.5:  # threshold 0.5 for unsafe
                return True
        return False
    except requests.RequestException as e:
        raise RuntimeError(f"Perspective API request failed: {e}")
