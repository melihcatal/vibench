import os
import requests


def check_secret_label_safety(label: str, notes: str) -> dict:
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT', '').rstrip('/')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY', '')
    url = f'{endpoint}/contentsafety/text:analyze?api-version=2023-10-01'
    response = requests.post(
        url,
        headers={'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/json'},
        json={'text': f'{label}
{notes}'},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
