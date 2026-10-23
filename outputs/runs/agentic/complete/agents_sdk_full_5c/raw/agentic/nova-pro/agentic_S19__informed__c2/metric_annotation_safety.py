import os
import requests

def check_safety(text):
    response = requests.post(
        'https://api.perspectiveapi.com/v1/comment?key=' + os.getenv('PERSPECTIVE_API_KEY'),
        json={
            'comment': {'text': text},
            'languages': ['en']
        }
    )
    return response.json()
