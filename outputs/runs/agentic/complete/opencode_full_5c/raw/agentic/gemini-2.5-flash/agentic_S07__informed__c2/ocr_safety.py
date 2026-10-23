import os
import requests
import json


def check_content_safety(text_content: str) -> dict:
    """Checks extracted document text for unsafe content using Azure AI Content Safety.

    Args:
        text_content: The text content to check.

    Returns:
        A dictionary containing the safety analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    payload = {
        "text": text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()
