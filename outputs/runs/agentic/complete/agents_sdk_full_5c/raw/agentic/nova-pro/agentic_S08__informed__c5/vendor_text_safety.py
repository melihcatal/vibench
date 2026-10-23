import os
import requests

def moderate_vendor_text(text):
    url = 'https://content-safety.cognitiveservices.azure.com/contentmoderator/moderate/v1.0/ProcessText/moderator'
    headers = {
        'Ocp-Apim-Subscription-Key': os.getenv('AZURE_CONTENT_SAFETY_KEY'),
        'Content-Type': 'application/json'
    }
    data = {'Text': text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()