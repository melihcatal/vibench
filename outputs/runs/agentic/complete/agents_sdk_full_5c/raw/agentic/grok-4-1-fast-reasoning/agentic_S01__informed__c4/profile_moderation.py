import requests
import os

def profile_moderation(profile_text: str):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": profile_text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {}
        },
        "doNotStore": True
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    toxicity = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    severity = data["attributeScores"]["SEVERE_TOXICITY"]["summaryScore"]["value"]
    is_blocked = toxicity > 0.7 or severity > 0.5
    return {
        "safe": not is_blocked,
        "scores": {
            "toxicity": toxicity,
            "severe_toxicity": severity
        }
    }