import os
import requests
from typing import Dict, Any


def check_payload_safety(text: str) -> Dict[str, Any]:
    """
    Checks decrypted text payloads for unsafe content using Azure AI Content Safety.
    
    Args:
        text: The text to analyze.
    
    Returns:
        A dictionary containing safety analysis results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set.")
    
    url = f"{endpoint}/contentsafety/text:analyze"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    
    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "breakByBlock": False
    }
    
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    
    return {
        "provider": "azure_content_safety",
        "results": response.json()
    }