import os
import requests

def check_text_safety(text):
    url = 'https://api.perspectiveapi.com/v1alpha1/comment/analyze'
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

text = 'This is an example log message.'
safety_check = check_text_safety(text)
print(safety_check)