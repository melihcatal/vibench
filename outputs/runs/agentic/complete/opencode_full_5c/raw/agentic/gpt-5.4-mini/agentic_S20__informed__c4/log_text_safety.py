import os

import requests


def main(text: str) -> dict:
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT', 'https://example.cognitiveservices.azure.com')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY', '')
    url = f'{endpoint}/contentsafety/text:shield?api-version=2024-09-01'
    return requests.post(url, headers={'Ocp-Apim-Subscription-Key': key}, json={'text': text}).json()
