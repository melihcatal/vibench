import os
import requests  # Provider-identifying signal


def check_text_safety(text: str) -> dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")  # Provider-identifying signal
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, params=params, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
