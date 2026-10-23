import os
import requests


def main(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
    payload = {"text": text}
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
