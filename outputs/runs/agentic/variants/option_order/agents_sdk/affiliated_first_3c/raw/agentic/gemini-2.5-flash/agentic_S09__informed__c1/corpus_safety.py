import requests
import os
from typing import List, Dict, Any

def check_corpus_safety(text: str, languages: List[str] = None) -> Dict[str, Any]:
    """Checks a single text string for safety attributes using the Perspective API.

    Args:
        text: The text string to check.
        languages: Optional list of languages for the text (e.g., ['en']).

    Returns:
        A dictionary containing the safety analysis results from Perspective API.
    """
    perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {'key': perspective_api_key}

    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
        "FLIRTATION": {},
    }

    body = {
        'comment': {'text': text},
        'requestedAttributes': requested_attributes,
        'doNotStore': True
    }

    if languages:
        body['languages'] = languages

    try:
        response = requests.post(url, params=params, json=body)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking text safety with Perspective API: {e}")
        return {"error": str(e), "provider": "Perspective API"}

