import os
import requests

# Simple toxicity check using Perspective API (content moderation)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
BASE_URL = "https://commentanalyzer.googleapis.com/v1beta3/comments:analyze"

def check_ocr_safety(text):
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
    }
    headers = {
        "X-API-KEY": PERSPECTIVE_API_KEY,
        "Content-Type": "application/json"
    }
    resp = requests.post(BASE_URL, json=payload, headers=headers)
    resp.raise_for_status()
    scores = resp.json()["attributeScores"]
    toxicity = scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    severe = scores.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
    return toxicity, severe
