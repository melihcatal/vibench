import os
import requests
from typing import List, Dict, Any

from vision_models import ImageLabel

def check_labels_for_toxicity(labels: List[ImageLabel]) -> Dict[str, Any]:
    """
    Checks a list of visual labels for unsafe text attributes using the Google Perspective API.
    
    Args:
        labels: A list of ImageLabel objects.
    
    Returns:
        A dictionary containing the analysis results from the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
        
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    text_to_check = ", ".join([label.name for label in labels])

    payload = {
        'comment': {'text': text_to_check},
        'languages': ['en'],
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    return response.json()
