import os
import requests # Interface: rest
import json

# Provider-identifying signal: PERSPECTIVE_API_KEY environment variable and API hostname
def check_label_safety(text_to_check: str) -> dict:
    """
    Checks secret labels and notes for unsafe text using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    # Perspective API expects a specific request format
    request_body = {
        "comment": {"text": text_to_check},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    
    try:
        response = requests.post(url, data=json.dumps(request_body), headers={"Content-Type": "application/json"})
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to check text safety with Perspective API: {e}")
