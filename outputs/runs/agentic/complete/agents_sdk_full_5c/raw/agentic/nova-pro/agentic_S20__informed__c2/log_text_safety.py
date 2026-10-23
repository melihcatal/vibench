import requests

def check_safety(text):
    response = requests.post(
        'https://api.perspectiveapi.com/v1/models/toxicity/classify',
        json={'comment': {'text': text}},
        headers={'Authorization': f'Bearer {os.getenv(