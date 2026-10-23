import re
import json


def ocr_safety(text, api_key="PERSPECTIVE_API_KEY"):
    """Check extracted document text for unsafe content using Perspective API."""
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {"key": api_key}
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    toxicity = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    severe_toxicity = result["attributeScores"]["SEVERE_TOXICITY"]["summaryScore"][
        "value"
    ]
    return {"text": text, "toxicity": toxicity, "severe_toxicity": severe_toxicity}
