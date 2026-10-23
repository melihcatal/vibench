import os
import requests
from typing import Dict, Any


def moderate_transcript(text_to_moderate: str) -> Dict[str, Any]:
    """
    Moderates transcript text using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    payload = {"text": text_to_moderate}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
