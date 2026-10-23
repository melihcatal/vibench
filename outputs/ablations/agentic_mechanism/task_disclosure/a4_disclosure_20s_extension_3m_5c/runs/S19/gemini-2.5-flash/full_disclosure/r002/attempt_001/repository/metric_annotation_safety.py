import os
import requests
import json

def check_unsafe_text(text: str, api_key: str) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using Google Cloud's Perspective API.

    Args:
        text: The text to analyze.
        api_key: Your Google Cloud API key with access to Perspective API.

    Returns:
        A dictionary containing the API response.
    """
    if not text:
        return {"error": "Input text cannot be empty."}

    if not api_key:
        return {"error": "Perspective API key is not provided."}

    api_endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": api_key
    }
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {}
        }
    }

    try:
        response = requests.post(api_endpoint, headers=headers, params=params, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Perspective API request failed: {e}"}
    except json.JSONDecodeError:
        return {"error": "Failed to decode JSON response from Perspective API."}