import os
import requests
import json

def moderate_text_azure_content_safety(text: str) -> dict:
    """Moderates text using Azure AI Content Safety API."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    api_version = "2023-10-01"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }

    data = {
        "text": text
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error moderating text with Azure AI Content Safety: {e}")
        raise
