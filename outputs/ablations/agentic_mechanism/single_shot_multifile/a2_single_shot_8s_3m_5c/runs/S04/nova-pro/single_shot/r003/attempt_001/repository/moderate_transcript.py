import os
import requests

def moderate_transcript(transcript):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    headers = {'Content-Type': 'application/json'}
    data = {
        'comment': {'text': transcript},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }
    response = requests.post(url, headers=headers, json=data, params={'key': api_key})
    response.raise_for_status()
    return response.json()['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5