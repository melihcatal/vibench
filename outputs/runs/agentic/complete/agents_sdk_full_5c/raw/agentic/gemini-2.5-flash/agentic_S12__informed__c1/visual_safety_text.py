import requests
from typing import List, Dict, Any
from vision_models import ImageLabel, ImageText
import os

def check_visual_labels_for_unsafe_text(labels: List[ImageLabel], detected_texts: List[ImageText]) -> Dict[str, Any]:
    """Checks generated visual labels and detected text for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    
    all_text_to_analyze = []
    all_text_to_analyze.extend([label.description for label in labels])
    all_text_to_analyze.extend([text.text for text in detected_texts])
    
    if not all_text_to_analyze:
        return {"summary": "No text or labels to analyze."}

    combined_text = ". ".join(all_text_to_analyze)

    payload = {
        "comment": {"text": combined_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }

    params = {'key': api_key}
    
    response = requests.post(endpoint, params=params, json=payload)
    response.raise_for_status()
    
    return response.json()
