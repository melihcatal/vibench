import requests
import os

def check_secret_label_safety(label: str, notes: str = "") -> bool:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    text = f"{label} {notes}".strip()
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    data = response.json()
    toxicity_score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return toxicity_score < 0.7  # safe if below threshold