import os
import requests
import json

def check_content_safety(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    data = {
        "text": text
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
