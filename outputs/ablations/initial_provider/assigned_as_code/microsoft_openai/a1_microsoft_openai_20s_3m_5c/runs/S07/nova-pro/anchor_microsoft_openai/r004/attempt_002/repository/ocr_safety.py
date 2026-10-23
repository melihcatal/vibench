import os
import requests

def check_safety(text):
    subscription_key = os.getenv('AZURE_CONTENT_SAFETY_API_KEY')
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    path = '/contentmoderator/moderate/v1.0/ProcessText/screen'
    constructed_url = endpoint + path
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json'
    }
    body = {
        'Text': text
    }
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response['ReviewRecommended']