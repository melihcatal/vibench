import os
import requests

def check_unsafe_content(text: str) -> dict:
    # PERSPECTIVE_API_KEY environment variable should be set
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    requested_attributes = {
        'TOXICITY': {},
        'SEVERE_TOXICITY': {},
        'IDENTITY_ATTACK': {},
        'INSULT': {},
        'PROFANITY': {},
        'THREAT': {}
    }

    data = {
        'comment': {'text': text},
        'requestedAttributes': requested_attributes,
        'languages': ['en'] # Assuming English for safety check, can be made dynamic if needed
    }

    response = requests.post(url, json=data)
    response.raise_for_status() # Raise an exception for HTTP errors

    return response.json()
