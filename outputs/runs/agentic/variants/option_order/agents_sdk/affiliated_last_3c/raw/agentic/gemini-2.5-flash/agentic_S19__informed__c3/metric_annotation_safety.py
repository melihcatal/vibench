import requests
import os

def check_annotation_safety(text: str, client_id: str = None, api_key: str = None):
    """
    Checks free-text metric labels or annotations for unsafe text using Perspective API.

    Args:
        text: The free-text annotation or label to check.
        client_id: Your Perspective API client ID.
        api_key: Your Perspective API key.
    """
    # Perspective API usually uses an API key directly without a client ID in the typical sense for public endpoints.
    # The API key is often passed as a query parameter or header.
    # For simplicity, we'll assume the API_KEY is set as an environment variable or passed directly.
    # The endpoint below is a common pattern for Google Cloud APIs (which Perspective API is part of).

    perspective_api_key = api_key if api_key else os.environ.get('PERSPECTIVE_API_KEY')
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY must be provided or set as an environment variable.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"

    payload = {
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

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "details": response.text if 'response' in locals() else "No response"}

