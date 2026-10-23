import os
import requests


def check_prompt_safety(text: str) -> dict:
    endpoint = os.getenv("PERSPECTIVE_API_ENDPOINT", "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze")
    params = {"key": os.getenv("PERSPECTIVE_API_KEY", ""), "alt": "json"}
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}, "INSULT": {}, "THREAT": {}}}
    response = requests.post(endpoint, params=params, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
