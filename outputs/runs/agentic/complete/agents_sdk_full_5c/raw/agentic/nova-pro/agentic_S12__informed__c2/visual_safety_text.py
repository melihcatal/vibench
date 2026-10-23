import os
import requests

def check_safety(text):
    url = 'https://api.perspectiveapi.com/v1/comment'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer YOUR_PERSPECTIVE_API_KEY'}
    payload = {'comment': {'text': text}}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    safety_check = check_safety('This is a description of an image.')
    print(safety_check)