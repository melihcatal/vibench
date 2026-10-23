import os
import requests


def check_text_safety(text: str) -> dict:
    """
    Checks corpus text for safety before embedding using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT is not set")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}

    payload = {"text": text, "categories": ["Hate", "Sexual", "SelfHarm", "Violence"]}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
