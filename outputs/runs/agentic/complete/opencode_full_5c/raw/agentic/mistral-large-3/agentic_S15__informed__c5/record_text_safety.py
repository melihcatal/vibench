import requests
import os
from typing import Dict, Any, List


def check_text_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Checks user-generated document fields for unsafe content using Azure AI Content Safety.

    Args:
        texts: List of text fields to check

    Returns:
        List of safety analysis results
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set"
        )

    url = f"{endpoint}/contentsafety/text:analyze"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    results = []
    for text in texts:
        payload = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels",
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        results.append({"text": text, "safety_results": response.json()})

    return results
