from typing import Dict, Any, List
import requests

def check_text_safety(document: Dict[str, Any], text_fields: List[str]) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using Google Cloud's Perspective API.
    """
    perspective_api_key = "your-perspective-api-key"
    perspective_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"
    
    results = {}
    for field in text_fields:
        if field in document:
            text = document[field]
            payload = {
                "comment": {"text": text},
                "requestedAttributes": {"TOXICITY": {}}
            }
            response = requests.post(perspective_url, json=payload)
            results[field] = response.json()
    
    return results