import os
import requests


def profile_moderation(text: str) -> dict:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    response = requests.post(f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01", json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
