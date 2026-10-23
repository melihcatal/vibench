import os

import requests


def record_text_safety(text):
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required"
        )
    url = endpoint.rstrip("/") + "/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    return requests.post(url, headers=headers, json=payload, timeout=30).json()
