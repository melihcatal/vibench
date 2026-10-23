import os
import requests

# Perspective API: service=Perspective API; sdk=requests; interface=rest; auth=PERSPECTIVE_API_KEY

def check_prompt_safety(text: str) -> dict:
    """
    Checks prompts and generated text for unsafe content using Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
