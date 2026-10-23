import os
import requests
from typing import Dict, Any


def check_payload_safety(text: str) -> Dict[str, Any]:
    """
    Checks decrypted text payloads for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key
    }

    body = {
        'text': text
    }

    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze",
        headers=headers,
        json=body
    )
    response.raise_for_status()

    return response.json()