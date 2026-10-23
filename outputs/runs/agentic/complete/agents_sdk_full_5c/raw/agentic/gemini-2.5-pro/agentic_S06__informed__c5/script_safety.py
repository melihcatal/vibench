import os
import requests
import json

def check_script_safety(text: str) -> dict:
    """
    Checks a script for unsafe content using Azure AI Content Safety.

    Args:
        text: The text to analyze.

    Returns:
        The analysis result from the API as a dictionary.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    
    payload = {
        "text": text,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    
    return response.json()
