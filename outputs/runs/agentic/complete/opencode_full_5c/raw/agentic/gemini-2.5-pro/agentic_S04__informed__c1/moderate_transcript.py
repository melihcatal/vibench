import os
import requests
import json
from typing import Dict


def moderate_transcript(text_content: str) -> Dict:
    """
    Moderates transcript text using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}

    payload = {
        "text": text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    return response.json()
