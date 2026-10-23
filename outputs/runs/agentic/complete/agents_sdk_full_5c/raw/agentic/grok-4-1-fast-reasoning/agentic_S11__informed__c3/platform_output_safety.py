import os
import requests
import json

def check_platform_output_safety(text: str, threshold: float = 0.5) -> dict:
    """
    Check safety using Perspective API.
    """
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        scores = response.json().get("attributeScores", {})
        score_values = {k: v["summaryScore"]["value"] for k, v in scores.items()}
        is_safe = all(score_values.get(k, 0) < threshold for k in score_values)
        return {"safe": is_safe, "scores": score_values}
    return {"safe": True, "error": "API request failed"}