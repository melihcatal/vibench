import os
import requests

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

def check_annotation_safety(annotation):
    response = requests.post(
        'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + PERSPECTIVE_API_KEY,
        json={
            'comment': {'text': annotation},
            'languages': ['en']
        }
    )
    return response.json()