import os
import requests


def moderate_transcript(text):
    response = requests.post(
        'https://api.perspectiveapi.com/v1/comment',
        params={'key': os.environ['PERSPECTIVE_API_KEY'], 'text': text},
        timeout=30
    )
    response.raise_for_status()
    return response.json()['attributeScores']