from typing import Dict, Any, List
import requests
from database_models import DocumentResponse

def check_text_safety(document: DocumentResponse) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using Google Cloud's Perspective API.
    
    Args:
        document: The document to check.
        
    Returns:
        A dictionary containing safety attributes and scores.
    """
    api_key = "<your-google-cloud-api-key>"  # Replace with a valid Google Cloud API key
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    text_content = " ".join([str(v) for v in document.data.values() if isinstance(v, str)])
    payload = {
        "comment": {"text": text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {}
        }
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()