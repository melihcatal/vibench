from typing import Dict, Any
import requests
import os

def check_output_safety(text: str) -> Dict[str, Any]:
    """
    Checks Azure OpenAI model output for unsafe content using Azure Content Safety API.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_API_KEY")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json"
    }

    body = {
        "text": text,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"]
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()