import os
import requests


def check_unsafe_content(text: str) -> dict:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # The ANALYZE_TEXT_REQUEST documentation specifies the format.
    # See https://developers.perspectiveapi.com/s/docs-sample-requests
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
        "languages": ["en"],  # Specify language for analysis
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
