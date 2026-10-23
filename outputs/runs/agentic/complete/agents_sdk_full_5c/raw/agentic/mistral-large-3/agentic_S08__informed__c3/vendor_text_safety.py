import os
import requests
from typing import Dict, Any


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "breakByBlock": False,
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    return response.json()