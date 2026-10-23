import requests
import os

# Perspective API endpoint and key from environment variables
# PERSPECTIVE_API_KEY should be set
# The API endpoint is generally fixed for public API.

def moderate_transcript_text(text: str) -> dict:
    """
    Moderates transcript text using the Perspective API.
    Requires PERSPECTIVE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=" + api_key
    
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": requested_attributes,
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()
        print(f"Perspective API moderation successful for text: '{text[:50]}...'")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}
