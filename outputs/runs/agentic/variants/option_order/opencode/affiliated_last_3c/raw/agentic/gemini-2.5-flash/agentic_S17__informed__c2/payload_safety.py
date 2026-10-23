import requests
import os
import json


def check_payload_safety_azure(
    text_payload: str, endpoint: str = None, key: str = None
) -> dict:
    """Checks a text payload for unsafe content using Azure AI Content Safety."""
    if endpoint is None:
        endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    if key is None:
        key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be provided or set as environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": text_payload,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

    return response.json()
