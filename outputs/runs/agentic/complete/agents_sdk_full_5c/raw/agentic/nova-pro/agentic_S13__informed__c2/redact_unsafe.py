import os
import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')

def redact_unsafe(text):
    url = AZURE_CONTENT_SAFETY_ENDPOINT + '/text/moderation/v1.0/screen'
    headers = {'Ocp-Apim-Subscription-Key': AZURE_CONTENT_SAFETY_KEY, 'Content-Type': 'application/json'}
    payload = {'text': text}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()