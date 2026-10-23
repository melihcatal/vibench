import os
import requests
import json

def moderate_profile_text(profile_text: str) -> dict:
    """
    Moderates profile text using Google Cloud Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Google Cloud Perspective API endpoint
    # Provider-identifying signal: API hostname
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    # Provider-identifying signal: specific analysis types
    data = {
        "comment": {"text": profile_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}
