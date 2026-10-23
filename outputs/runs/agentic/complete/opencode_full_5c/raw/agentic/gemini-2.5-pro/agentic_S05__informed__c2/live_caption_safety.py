import os
import requests
import json


def check_unsafe_content(text: str):
    """
    Checks for unsafe content in a live transcript using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure Content Safety endpoint or key not set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure AI Content Safety API: {e}")
        return None
