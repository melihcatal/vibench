import os
import requests

def moderate_transcript(transcript):
    api_key = os.getenv('GOOGLE_CLOUD_CONTENT_MODERATOR_API_KEY')
    url = 'https://contentmoderator.cognitiveservices.azure.com/contentmoderator/moderate/v1.0/ProcessText/Moderate'
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'Text': transcript
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()['Result']['Status'] == 'True'