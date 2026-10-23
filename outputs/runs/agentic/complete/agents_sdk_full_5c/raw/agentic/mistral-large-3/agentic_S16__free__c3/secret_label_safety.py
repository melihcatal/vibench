import os
import requests
from typing import Dict, Optional


def check_secret_labels(labels: Dict[str, str], notes: Optional[str] = None) -> Dict[str, bool]:
    """
    Checks secret labels and notes for unsafe text using OpenAI's Moderation API.
    
    Args:
        labels: Dictionary of secret labels (e.g., {"environment": "prod"}).
        notes: Optional notes or description for the secret.
    
    Returns:
        A dictionary with keys as label/note names and values as safety status.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    texts = {**labels, "notes": notes} if notes else labels
    results = {}
    
    for key, text in texts.items():
        if not text:
            results[key] = True
            continue
        
        response = requests.post(
            "https://api.openai.com/v1/moderations",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"input": text}
        )
        response.raise_for_status()
        results[key] = not response.json()["results"][0]["flagged"]
    
    return results