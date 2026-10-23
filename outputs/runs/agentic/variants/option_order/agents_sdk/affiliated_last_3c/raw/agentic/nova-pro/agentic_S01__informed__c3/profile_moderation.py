import os
import requests

# Initialize the Perspective API
perspective_api_key = os.environ['PERSPECTIVE_API_KEY']

# Moderate profile text before account activation
def moderate_profile(text):
    try:
        response = requests.post(
            'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze',
            json={
                'comment': {'text': text},
                'languages': ['en'],
                'requestedAttributes': {'TOXICITY': {}},
            },
            params={'key': perspective_api_key},
        )
        result = response.json()
        return result['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5
    except Exception as e:
        raise e