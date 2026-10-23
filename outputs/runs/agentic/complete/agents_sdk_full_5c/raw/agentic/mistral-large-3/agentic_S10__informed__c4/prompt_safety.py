import os
import requests
from typing import Dict, Any


def check_prompt_safety(text: str) -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured.")
    
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    return response.json()