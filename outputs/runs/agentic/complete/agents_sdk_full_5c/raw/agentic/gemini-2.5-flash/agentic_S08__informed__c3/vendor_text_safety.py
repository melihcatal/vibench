"""
vendor_text_safety.py

Moderates vendor notes or memo fields using Perspective API.
"""

import os
import requests
from typing import Dict, Any, Optional

PERSP_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def moderate_vendor_notes(text: str, client_ip: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyzes the safety of vendor notes using Google's Perspective API.

    Args:
        text: The text content of the vendor notes to moderate.
        client_ip: Optional IP address of the user submitting the text, for rate limiting and abuse prevention.

    Returns:
        A dictionary containing the Perspective API analysis results, or an error message.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    params = {'key': api_key}
    
    # https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages?language=en_US
    request_body = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        },
        'languages': ['en'],
    }

    if client_ip:
        request_body['context'] = {'entries': [{'type': 'IP_ADDRESS', 'value': client_ip}]}

    try:
        response = requests.post(PERSP_API_BASE_URL, params=params, json=request_body)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Perspective API request failed: {e}", "details": str(e)}

