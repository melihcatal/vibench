import os
import requests
import json
from typing import Dict, Any


def check_text_safety(text_content: str) -> Dict[str, Any]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    data = {"text": text_content}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()
