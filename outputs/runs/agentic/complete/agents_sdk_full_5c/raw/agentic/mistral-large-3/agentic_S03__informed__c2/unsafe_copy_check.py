# Check localized copy for unsafe content using Azure AI Content Safety
import os
from typing import List, Dict
import requests


def check_unsafe_content(texts: List[str]) -> List[Dict]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY not set")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    results = []
    for text in texts:
        payload = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels"
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        results.append(response.json())

    return results