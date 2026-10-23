import os
from googleapiclient import discovery
from typing import Dict, Any, List


def get_perspective_client():
    """Initialize and return the Perspective API client." ""
    return discovery.build(
        "commentanalyzer", 
        "v1alpha1", 
        developerKey=os.getenv("PERSPECTIVE_API_KEY"),
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )


def check_text_safety(text: str) -> Dict[str, Any]:
    """
    Checks user-generated text for unsafe content using Perspective API.
    
    Args:
        text: The text to analyze.
        
    Returns:
        A dictionary containing toxicity scores and attributes.
    """
    client = get_perspective_client()
    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }
    
    response = client.comments().analyze(body=analyze_request).execute()
    return response