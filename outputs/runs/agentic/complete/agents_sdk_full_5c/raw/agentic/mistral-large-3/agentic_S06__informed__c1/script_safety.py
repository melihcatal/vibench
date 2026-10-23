import os
import requests
from typing import Dict, List

def check_script_safety(
    text: str,
    api_key: str = None,
    endpoint: str = None
) -> Dict:
    """
    Check narration scripts for unsafe content using Azure AI Content Safety.
    """
    api_key = api_key or os.getenv("AZURE_CONTENT_SAFETY_KEY")
    endpoint = endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    
    if not api_key or not endpoint:
        raise ValueError("Azure Content Safety API key and endpoint must be provided.")
    
    url = f"{endpoint}/contentsafety/text:analyze"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "breakByBlock": False
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    return response.json()