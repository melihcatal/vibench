import os
import requests

API_URL = 'https://api.cognitive.microsoft.com/contentmoderator/moderate/v1.0/ProcessText/moderate'

def moderate_text(text):
    headers = {
        'Ocp-Apim-Subscription-Key': os.getenv('AZURE_CONTENT_SAFETY_KEY'),
        'Content-Type': 'application/json'
    }
    data = {
        'Text': text
    }
    response = requests.post(API_URL, json=data, headers=headers)
    return response.json()