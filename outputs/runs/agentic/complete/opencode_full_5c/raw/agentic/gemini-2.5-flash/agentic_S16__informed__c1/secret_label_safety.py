import os
import requests
import json


def secret_label_safety(text: str) -> dict:
    """Checks secret labels and notes for unsafe text using Azure AI Content Safety.

    Args:
        text: The text content to check for safety.

    Returns:
        A dictionary containing the safety analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY environment variables not set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    data = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()
