import os
import requests
from typing import Dict, Any

# Ensure PERSPECTIVE_API_KEY environment variable is set
PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")

def check_annotation_safety(text: str) -> Dict[str, Any]:
    """Checks free-text metric labels or annotations for unsafe text using Perspective API."""
    if not PERSPECTIVE_API_KEY:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    # Perspective API endpoint
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"

    # Request body for content safety analysis
    data = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        },
        'languages': ['en']
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error calling Perspective API: {e}"}
