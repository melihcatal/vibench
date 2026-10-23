import os
import requests

def moderate_transcript(transcript):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    payload = {
        'comment': {'text': transcript},
       'requestedAttributes': {'TOXICITY': {}}
    }
    headers = {'Content-Type': 'application/json'}
    params = {'key': api_key}
    response = requests.post(url, json=payload, params=params, headers=headers)
    analysis = response.json()
    toxicity_score = analysis['attributeScores']['TOXICITY']['summaryScore']['value']
    if toxicity_score > 0.5:
        raise ValueError('Transcript contains toxic language')
    return transcript