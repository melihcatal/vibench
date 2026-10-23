import os
from typing import Dict, List, Optional
import requests

from security_models import AuditNote


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_label_safety(
    labels: Optional[List[str]] = None,
    notes: Optional[List[str]] = None,
) -> Dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    if labels is None:
        labels = []
    if notes is None:
        notes = []

    combined_text = " ".join(labels + notes)
    if not combined_text.strip():
        return {"safe": True, "scores": {}, "flagged_items": []}

    payload = {
        "comment": {"text": combined_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    params = {"key": api_key}

    response = requests.post(
        PERSPECTIVE_API_URL,
        json=payload,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    result = response.json()
    attribute_scores = result.get("attributeScores", {})

    threshold = 0.7
    flagged_items = []
    scores = {}

    for attr_name, attr_data in attribute_scores.items():
        score_value = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score_value
        if score_value >= threshold:
            flagged_items.append(
                {
                    "attribute": attr_name,
                    "score": score_value,
                    "threshold": threshold,
                }
            )

    is_safe = len(flagged_items) == 0

    return {
        "safe": is_safe,
        "scores": scores,
        "flagged_items": flagged_items,
        "input_text": combined_text,
        "provider": "perspective-api",
    }


def check_audit_note_safety(note: AuditNote) -> Dict:
    return check_label_safety(
        labels=note.labels,
        notes=[note.note_text],
    )


if __name__ == "__main__":
    test_labels = ["production", "database", "rotate-immediately"]
    test_notes = ["This secret contains sensitive credentials for the payment system"]
    result = check_label_safety(labels=test_labels, notes=test_notes)
    import json

    print(json.dumps(result, indent=2))
