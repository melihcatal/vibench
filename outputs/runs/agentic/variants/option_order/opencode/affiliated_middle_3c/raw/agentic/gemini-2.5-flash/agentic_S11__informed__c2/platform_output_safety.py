import os
import requests
import json


def check_platform_output_safety(text: str) -> dict:
    azure_content_safety_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    azure_content_safety_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not azure_content_safety_endpoint or not azure_content_safety_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    api_version = "2023-04-30-preview"
    url = f"{azure_content_safety_endpoint}/contentsafety/text:analyze?api-version={api_version}"
    headers = {
        "Ocp-Apim-Subscription-Key": azure_content_safety_key,
        "Content-Type": "application/json",
    }
    payload = {"text": text}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    return response.json()
