import os
import requests
import json


def is_safe_content(script: str, threshold: float = 0.5) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": script},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    response = requests.post(url, json=payload)
    result = response.json()
    toxicity = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    severe = result["attributeScores"]["SEVERE_TOXICITY"]["summaryScore"]["value"]
    return {
        "is_safe": toxicity < threshold,
        "toxicity_score": toxicity,
        "severe_score": severe,
    }
