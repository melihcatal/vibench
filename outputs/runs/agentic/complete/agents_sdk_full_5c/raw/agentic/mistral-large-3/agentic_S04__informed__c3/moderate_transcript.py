import os
import requests
from typing import List, Dict

def moderate_transcript(segments: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Moderates transcript segments using Perspective API.
    Returns moderated segments with toxicity scores.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    moderated_segments = []
    for segment in segments:
        payload = {
            "comment": {"text": segment["text"]},
            "requestedAttributes": {"TOXICITY": {}}
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        toxicity_score = response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        
        moderated_segments.append({
            **segment,
            "toxicity": toxicity_score
        })
    
    return moderated_segments