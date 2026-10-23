# [LATER-STEP] record_text_safety.py
# Detect unsafe content in user‑generated document fields using Perspective API

import os
import requests
import json

# Perspective API configuration
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)

PARAMS = {
    "key": PERSPECTIVE_API_KEY,
    "requestedAttributes": {"TOXICITY": {}, "SPAM": {}},
}


def check_safety(document_fields, attribute="TOXICITY"):
    """Run content moderation on specific document fields.

    Args:
        document_fields (dict): Key/value pairs to scan.
        attribute (str): Perspective attribute to check (default TOXICITY).

    Returns:
        dict: {field_name: score} where score is in [0.0, 1.0].
    """
    payload = {
        "comment": {
            "type": "PLAIN_TEXT",
            "text": json.dumps(document_fields),  # simple concatenation for demo
        },
        "languages": ["en"],
        "requestedAttributes": {attribute: {}},
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, params=PARAMS, json=payload)
    response.raise_for_status()
    attrs = response.json()["attributeScores"][attribute]["summaryScore"]
    score = attrs["value"]
    return score


# Example usage:
# fields = {'comment': 'Buy cheap viagra now!'}
# print(check_safety(fields))
