import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

def check_live_caption_safety(text: str) -> bool:
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    response = requests.post(url, json=payload)
    data = response.json()
    toxicity_score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return toxicity_score > 0.7  # unsafe
