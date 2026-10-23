import os
import requests
from typing import List
from speech_models import TranscriptionResponse

def moderate_transcript(transcript: TranscriptionResponse) -> Dict:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}
    data = {
        "comment": {"text": transcript.text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    
    response = requests.post(url, params=params, json=data)
    response.raise_for_status()
    
    return response.json()