import os
import requests

# PERSPECTIVE API integration
API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def score_text(user_text, attribute="TOXICITY"):
    """Scores user text using Perspective API and returns the toxicity score and severity.

    Returns:
        dict: { 'attribute': score, 'severity': <LOW/MEDIUM/HIGH> }
    """
    payload = {"comment": {"text": user_text}, "requestedAttributes": {attribute: {}}}
    headers = {"Content-Type": "application/json", "x-api-key": PERSPECTIVE_API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API error: {response.text}")
    result = response.json().get("attributeScores", {}).get(attribute, {})
    score = result.get("summaryScore", {}).get("value")
    severity = "LOW"
    if score >= 0.75:
        severity = "HIGH"
    elif score >= 0.5:
        severity = "MEDIUM"
    return {"attribute": attribute, "score": score, "severity": severity}
