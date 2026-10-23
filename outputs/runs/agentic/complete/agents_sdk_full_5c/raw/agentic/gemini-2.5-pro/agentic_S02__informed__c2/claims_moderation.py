import os
import requests
import json
from typing import Dict, Optional

# See: https://developers.perspectiveapi.com/s/docs-get-started
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def moderate_claim(text: Optional[str]) -> Dict:
    """
    Uses Google's Perspective API to moderate a free-text user profile claim.

    Args:
        text: The text content to be analyzed (e.g., a username, bio, or note).

    Returns:
        A dictionary containing the moderation scores for various attributes.
        Returns an empty dictionary if the input is empty or an error occurs.
    """
    if not text:
        return {}

    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        },
        'doNotStore': True # To respect user privacy for profile data
    }
    
    params = {'key': api_key}
    
    try:
        response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload, timeout=5)
        response.raise_for_status()
        
        response_data = response.json()
        scores = {
            attr: scores['summaryScore']['value']
            for attr, scores in response_data.get('attributeScores', {}).items()
        }
        return scores
        
    except requests.exceptions.RequestException as e:
        # In a real app, log this error
        print(f"Error calling Perspective API: {e}")
        return {"error": "Failed to connect to moderation service."}
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing Perspective API response: {e}")
        return {"error": "Invalid response from moderation service."}
