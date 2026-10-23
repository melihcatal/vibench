import os
import requests


def check_message_safety(text: str):
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    if not endpoint or not key:
        raise RuntimeError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required"
        )
    url = endpoint.rstrip("/") + "/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": text}
    return requests.post(url, headers=headers, json=payload, timeout=30).json()
