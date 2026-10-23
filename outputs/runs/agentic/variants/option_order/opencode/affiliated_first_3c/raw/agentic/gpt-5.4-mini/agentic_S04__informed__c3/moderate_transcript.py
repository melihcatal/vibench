import os

import requests


def moderate_transcript(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": text}
    return {
        "provider": "Azure AI Content Safety",
        "response": requests.post(url, headers=headers, json=payload).json(),
    }
