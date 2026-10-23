import requests
import os
from typing import Dict, Any


def check_output_safety(text: str) -> Dict[str, Any]:
    """Check text for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    url = f"{endpoint}/contentsafety/text:analyze"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        "outputType": "FourSeverityLevels"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    return response.json()