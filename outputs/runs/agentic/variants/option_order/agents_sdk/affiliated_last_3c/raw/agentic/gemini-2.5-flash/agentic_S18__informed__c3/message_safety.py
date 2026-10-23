import os
import requests
import json
from messaging_models import PubSubMessage

# Azure AI Content Safety provider-specific signal (endpoint hostname)
AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"

def check_message_safety(message: PubSubMessage) -> dict:
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)

    if not endpoint or not key:
        raise ValueError(f"Both {AZURE_CONTENT_SAFETY_ENDPOINT_ENV} and {AZURE_CONTENT_SAFETY_KEY_ENV} environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    text_content = str(message.data) # Assuming the message data can be converted to a string for analysis

    body = {
        "text": text_content,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return {"error": str(e), "details": e.response.text if hasattr(e, 'response') else "No response content"}
