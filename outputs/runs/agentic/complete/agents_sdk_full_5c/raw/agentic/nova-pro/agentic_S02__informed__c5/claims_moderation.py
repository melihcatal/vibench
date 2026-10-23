import os
import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
AZURE_CONTENT_SAFETY_KEY = os.getenv('AZURE_CONTENT_SAFETY_KEY')

def claims_moderation(claims):
    url = f'{AZURE_CONTENT_SAFETY_ENDPOINT}/moderation/v1/screen'
    headers = {'Ocp-Apim-Subscription-Key': AZURE_CONTENT_SAFETY_KEY}
    response = requests.post(url, json=claims, headers=headers)
    response.raise_for_status()
    return response.json()