import os
import requests

def moderate_transcript(transcript):
    api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    params = {'key': api_key}
    data = {
        'comment': {'text': transcript},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }
    response = requests.post(url, params=params, json=data)
    response.raise_for_status()
    return response.json()['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5