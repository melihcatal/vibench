import os
import requests

def message_safety(text):
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    resp = requests.post(f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01", headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}, json={"text": text})
    return resp.json()
