import os
import requests
from typing import List, Dict
from speech_models import SpeakerLabel


def moderate_transcript(segments: List[SpeakerLabel]) -> List[Dict]:
    """
    Moderate transcript text using Perspective API.
    Returns a list of moderation results for each segment.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = []
    
    for segment in segments:
        payload = {
            "comment": {"text": segment.text},
            "requestedAttributes": {"TOXICITY": {}}
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        results.append({
            "speaker": segment.speaker,
            "text": segment.text,
            "moderation": response.json()
        })
    
    return results