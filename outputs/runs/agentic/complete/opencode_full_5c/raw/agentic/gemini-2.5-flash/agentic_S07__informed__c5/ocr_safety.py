import requests
import os


def check_text_safety(
    text: str, api_key: str = os.environ.get("PERSPECTIVE_API_KEY")
) -> dict:
    """
    Checks text for unsafe content using Perspective API.
    """
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
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        },
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()
