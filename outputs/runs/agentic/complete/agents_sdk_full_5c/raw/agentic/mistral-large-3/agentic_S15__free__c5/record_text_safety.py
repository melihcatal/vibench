from typing import Dict, Any
import requests

def check_text_safety(document: Dict[str, Any], fields_to_check: list) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using Google Cloud's Perspective API.
    """
    api_key = "AIzaSy..."
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = {}
    
    for field in fields_to_check:
        text = document.get(field, "")
        data = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}}
        }
        response = requests.post(url, json=data)
        results[field] = response.json()
    
    return results