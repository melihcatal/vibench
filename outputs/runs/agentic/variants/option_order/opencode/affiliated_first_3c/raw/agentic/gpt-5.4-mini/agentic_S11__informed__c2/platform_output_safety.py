import os
import requests

def platform_output_safety(text: str):
    resp = requests.post(f"{os.environ['AZURE_CONTENT_SAFETY_ENDPOINT'].rstrip('/')}/contentsafety/text:analyze?api-version=2024-09-01", headers={'Ocp-Apim-Subscription-Key': os.environ['AZURE_CONTENT_SAFETY_KEY'], 'Content-Type': 'application/json'}, json={'text': text}, timeout=30)
    resp.raise_for_status()
    return resp.json()
