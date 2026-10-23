import os
import requests

def check_payload_safety(text: str, threshold: float = 0.7) -> dict:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANE": {}
        }
    }
    response = requests.post(url, json=payload)
    result = response.json()
    scores = {k: result['attributeScores'][k]['summaryScore']['value'] for k in result['attributeScores']}
    is_safe = all(scores.get(k, 0) < threshold for k in scores)
    return {"scores": scores, "is_safe": is_safe}