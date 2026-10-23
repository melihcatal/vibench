import os
import requests
from typing import List, Dict, Any


def check_corpus_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Check corpus texts for harmful content using Azure AI Content Safety.
    
    Args:
        texts: List of text strings to check.
    
    Returns:
        List of safety analysis results for each text.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    results = []
    for text in texts:
        headers = {
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels",
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        results.append(response.json())
    return results