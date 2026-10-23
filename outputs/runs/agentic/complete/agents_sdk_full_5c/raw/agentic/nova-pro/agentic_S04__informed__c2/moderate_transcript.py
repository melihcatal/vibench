import os
import requests

def moderate_transcript(transcript_text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'text': transcript_text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    headers = {'Content-Type': 'application/json', 'API-Key': api_key}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()