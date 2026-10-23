# Moderate profile text before account activation using Azure AI Content Safety

import os
import requests
from typing import Dict, Any


def moderate_profile_text(text: str) -> Dict[str, Any]:
    """
    Moderate user-provided profile text using Azure AI Content Safety.
    Model: Azure AI Content Safety (text moderation).
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()