import requests
import os

def check_secret_label_safety(text: str) -> dict:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {}
        },
        "languages": ["en"]
    }
    params = {"key": api_key}
    response = requests.post(url, json=payload, params=params)
    response.raise_for_status()
    result = response.json()
    # Normalize scores
    scores = {k: result["attributeScores"][k]["summaryScore"]["value"] for k in result["attributeScores"]}
    return {"safe": all(s < 0.5 for s in scores.values()), "scores": scores}