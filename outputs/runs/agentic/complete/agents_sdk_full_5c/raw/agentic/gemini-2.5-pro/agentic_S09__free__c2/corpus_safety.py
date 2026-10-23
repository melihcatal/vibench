import os
import requests
import json

def check_text_safety(corpus_text: str) -> dict:
    """
    Checks corpus text for harmful content using Azure AI Content Safety.

    Args:
        corpus_text: The text to analyze.

    Returns:
        A dictionary with the analysis results from the API.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }
    
    payload = {
        "text": corpus_text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    
    return response.json()
