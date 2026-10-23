import os
import requests


def check_log_safety(text: str) -> dict:
    response = requests.post(
        'https://api.perspectiveapi.com/v1alpha1/comments:analyze',
        params={'key': os.environ.get('PERSPECTIVE_API_KEY', '')},
        json={'comment': {'text': text}, 'languages': ['en']},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
