import os
import requests
import json

def check_text_for_safety(text_to_check: str) -> dict:
    """
    Checks text for harmful content using Azure AI Content Safety.

    Args:
        text_to_check: The text from a secret label or note.

    Returns:
        A dictionary with the analysis results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    # Provider-identifying hostname in the URL
    url = f"{endpoint}contentsafety/text:analyze?api-version=2023-10-01"
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }
    
    payload = {
        "text": text_to_check,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with Azure AI Content Safety request: {e}")
        raise
