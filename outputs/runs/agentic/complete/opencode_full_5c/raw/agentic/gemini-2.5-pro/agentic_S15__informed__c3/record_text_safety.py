import os
import requests
import json


def check_user_content_safety(text: str):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set.")

    url = f"{endpoint}contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": api_key}

    payload = {"text": text}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    return response.json()
