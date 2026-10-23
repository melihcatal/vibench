import os
import requests

def check_script_safety(text: str, api_key: str) -> dict:
    """
    Checks a narration script for unsafe content using Perspective API.
    Returns a dictionary of safety scores.
    """
    # Perspective API hostname
    API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    
    params = {
        "key": api_key,
    }
    
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"] # Assuming English for this example
    }

    response = requests.post(API_URL, params=params, json=data)
    response.raise_for_status() # Raise an exception for HTTP errors
    
    scores = {}
    attributes = response.json().get("attributeScores", {})
    for attr, details in attributes.items():
        scores[attr] = details.get("summaryScore", {}).get("value")
        
    return scores
