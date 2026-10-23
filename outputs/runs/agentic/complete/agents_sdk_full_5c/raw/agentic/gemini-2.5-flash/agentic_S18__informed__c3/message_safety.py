import requests
import os

def check_message_safety(text_payload: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set in environment variables.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    data = {
        "text": text_payload,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "outputType": "FourSeverityLevels"
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status() # Raise an exception for HTTP errors
    return response.json()
