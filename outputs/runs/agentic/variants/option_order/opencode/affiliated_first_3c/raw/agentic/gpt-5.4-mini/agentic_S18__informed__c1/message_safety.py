import os
import requests


def message_safety(text: str):
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
    response = requests.post(
        url,
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
    )
    response.raise_for_status()
    return response.json()
