import os
import requests
from typing import Dict, Any

def check_safety(text: str) -> Dict[str, Any]:
    """
    Checks text for unsafe content using Azure AI Content Safety API.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    # Azure AI Content Safety API hostname
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status() # Raise an exception for HTTP errors
    return response.json()
