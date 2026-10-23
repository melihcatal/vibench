# [LATER-STEP] metric_annotation_safety.py

# Check free‑text metric labels or annotations for unsafe text.
# Provider: Perspective API (requests REST client)

import os
import json
from typing import List, Dict

import requests


def check_annotations_for_unsafe_text(
    labels: List[str],
    api_key: str,
) -> List[Dict[str, Any]]:
    """
    Sends each *label* in *labels* to the Perspective API and returns a list of
    assessment results indicating toxicity scores and whether the text is flagged
    as unsafe.

    Returns a list of dicts: {label, score, is_unsafe}
    """
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }
    results = []
    for label in labels:
        payload = {
            "comment": {"text": label},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "PROFANITY": {},
            },
        }
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        score = (
            data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {})
        )
        is_unsafe = score.get("value", 0.0) > 0.8  # arbitrary unsafe threshold
        results.append(
            {
                "label": label,
                "toxicity_score": score.get("value"),
                "is_unsafe": is_unsafe,
            }
        )
    return results
