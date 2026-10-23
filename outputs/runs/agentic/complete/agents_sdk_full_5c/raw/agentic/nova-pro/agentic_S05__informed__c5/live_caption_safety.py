import os
import requests

def check_safety(text):
    url = 'https://api.perspectiveapi.com/v1/models/TOXICITY/analyze'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.getenv('PERSPECTIVE_API_KEY')
    }
    data = {
        'comment': {'text': text},
        'languages': ['en']
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()