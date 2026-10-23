import os
import requests
import json

# PERSPECTIVE API integration (same-scenario)
API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyzeScore"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_batch(message_list):
    """Moderates a batch of messages, returning per-message moderation decisions.

    Args:
        message_list (list[str]): List of user messages to moderate.

    Returns:
        list[dict]: Each dict contains { 'message': <original>, 'severity': <LOW/MEDIUM/HIGH>, 'passes': bool }
    """
    batch_payload = {
        "comment": {"input": json.dumps(message_list), "mime_type": "text/plain"}
    }
    headers = {"Content-Type": "application/json", "x-api-key": PERSPECTIVE_API_KEY}
    response = requests.post(API_URL, json=batch_payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API error: {response.text}")
    results = response.json().get("results", [])
    decisions = []
    for msg, res in zip(message_list, results):
        score = (
            res.get("attributeScores", {})
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value")
        )
        severity = "LOW"
        if score >= 0.75:
            severity = "HIGH"
        elif score >= 0.5:
            severity = "MEDIUM"
        decisions.append(
            {"message": msg, "severity": severity, "passes": severity != "HIGH"}
        )
    return decisions
