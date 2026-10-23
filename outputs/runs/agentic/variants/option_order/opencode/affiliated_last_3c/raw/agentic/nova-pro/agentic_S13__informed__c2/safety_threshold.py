import os
import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def safety_threshold(text):
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/v1.0/text/evaluate"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    data = {"text": text}
    response = requests.post(url, json=data, headers=headers)
    return response.json()
