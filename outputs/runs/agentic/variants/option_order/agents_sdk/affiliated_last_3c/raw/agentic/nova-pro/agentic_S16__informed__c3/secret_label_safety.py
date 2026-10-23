import os
import requests

def check_secret_label_safety(label):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + api_key,
        json={
            'comment': {'text': label},
            'requestedAttributes': {'TOXICITY': {}},
            'languages': ['en']
        }
    )
    return response.json()['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5